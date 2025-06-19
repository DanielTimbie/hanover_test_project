from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import requests
import openai
import os
from dotenv import load_dotenv
import json
from typing import List, Dict
from pathlib import Path
import random

load_dotenv()

# Create the templates directory if it doesn't exist
templates_dir = Path("templates")
templates_dir.mkdir(exist_ok=True)

app = FastAPI(title="Perplexity Clone", version="1.0.0")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure templates
templates = Jinja2Templates(directory=str(templates_dir))

# Configure APIs
openai.api_key = os.getenv("OPENAI_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

# Topics list - importing directly from topics.js would be complex,
# so we'll maintain it here as well
TOPICS = [
    "AI Ethics", "Quantum Computing", "Web3", "5G Networks", "Robotics",
    "Cybersecurity", "Space Tech", "Green Tech", "IoT", "Cloud Computing",
    "Black Holes", "Climate Change", "Genetics", "Neuroscience", "Renewable Energy",
    "Marine Biology", "Astronomy", "Evolution", "Particle Physics", "Biotechnology"
]

class PerplexityClone:
    def __init__(self):
        self.search_results = []
        self.conversation_history = []
    
    def clear_conversation(self):
        """Clear the conversation history"""
        self.conversation_history = []
        self.search_results = []
    
    def search_web(self, query: str) -> List[Dict]:
        """Search web using SerpAPI"""
        try:
            url = "https://serpapi.com/search"
            params = {
                "q": query,
                "api_key": SERPAPI_KEY,
                "num": 5  # Limit results for faster response
            }
            response = requests.get(url, params=params)
            data = response.json()
            
            results = []
            if "organic_results" in data:
                for result in data["organic_results"][:5]:
                    results.append({
                        "title": result.get("title", ""),
                        "snippet": result.get("snippet", ""),
                        "link": result.get("link", ""),
                        "position": result.get("position", 0)
                    })
            return results
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    def rerank_sources(self, sources: List[Dict], query: str) -> List[Dict]:
        """Rerank and filter sources based on the query using OpenAI."""
        try:
            # Format sources for the prompt
            sources_text = "\n".join([
                f"{i+1}. Title: {source['title']}\n   URL: {source['link']}\n   Snippet: {source['snippet']}"
                for i, source in enumerate(sources)
            ])
            
            prompt = f"""Given these search results and the user's query: "{query}", analyze the sources and decide:
1. Which sources should be excluded based on the query (e.g., if user asks to exclude certain sites or types of content)
2. Which remaining sources are most relevant to the query
3. The optimal order of sources based on relevance and user preferences

Search Results:
{sources_text}

Please provide your response in this JSON format:
{{
    "excluded_sources": [
        {{"index": 1, "reason": "Excluded because user requested to exclude this source type"}}
    ],
    "included_sources": [
        {{"index": 0, "reason": "Most relevant because..."}},
        {{"index": 2, "reason": "Second most relevant because..."}}
    ]
}}

Important rules:
1. If the query mentions excluding certain sources (e.g., "exclude Quora", "no Reddit", "without social media"), you MUST exclude those sources
2. If a source matches an exclusion criteria, it MUST go in excluded_sources
3. Only sources that pass all filters should be in included_sources
4. Rank remaining sources by relevance to the query

Response:"""

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful AI that analyzes and ranks search results based on relevance and user preferences. You must return valid JSON and strictly enforce source exclusion rules."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.2
            )
            
            try:
                reranking = json.loads(response.choices[0].message['content'])
                
                # Process excluded sources first
                excluded_indices = [item["index"] for item in reranking.get("excluded_sources", [])]
                excluded_sources = []
                for exclusion in reranking.get("excluded_sources", []):
                    if exclusion["index"] < len(sources):
                        source = sources[exclusion["index"]].copy()
                        source["exclusion_reason"] = exclusion.get("reason", "")
                        excluded_sources.append(source)
                
                # Only include sources that weren't excluded
                included_indices = [item["index"] for item in reranking.get("included_sources", [])]
                reranked_sources = []
                for i, ranking_info in enumerate(reranking.get("included_sources", [])):
                    idx = ranking_info["index"]
                    if idx < len(sources) and idx not in excluded_indices:
                        source = sources[idx].copy()
                        source["ranking_reason"] = ranking_info.get("reason", "")
                        reranked_sources.append(source)
                
                return {
                    "included": reranked_sources,
                    "excluded": excluded_sources
                }
                
            except json.JSONDecodeError:
                print("Error parsing OpenAI response as JSON")
                return {"included": sources, "excluded": []}
                
        except Exception as e:
            print(f"Reranking error: {e}")
            return {"included": sources, "excluded": []}

    def generate_ai_response(self, query: str, search_results: List[Dict], is_followup: bool = False, conversation_history: List[Dict] = None) -> Dict:
        """Generate AI response based on search results"""
        try:
            # Rerank sources for follow-up queries
            if is_followup:
                reranked_results = self.rerank_sources(search_results, query)
                search_results = reranked_results["included"]
                excluded_sources = reranked_results["excluded"]
            else:
                excluded_sources = []
            
            # Format search results for AI context
            context = "Search Results:\n"
            for i, result in enumerate(search_results, 1):
                context += f"{i}. {result['title']}\n"
                context += f"   {result['snippet']}\n"
                context += f"   Source: {result['link']}\n"
                if "ranking_reason" in result:
                    context += f"   Ranking: {result['ranking_reason']}\n"
                context += "\n"
            
            if excluded_sources:
                context += "\nExcluded Sources:\n"
                for i, result in enumerate(excluded_sources, 1):
                    context += f"{i}. {result['title']}\n"
                    context += f"   Reason: {result['exclusion_reason']}\n\n"
            
            # Add conversation history for follow-up queries
            conversation_context = ""
            if is_followup and conversation_history:
                conversation_context = "\nPrevious Conversation:\n"
                for i, msg in enumerate(conversation_history, 1):
                    conversation_context += f"Q{i}: {msg['query']}\n"
                    conversation_context += f"A{i}: {msg['answer']}\n\n"
                
                conversation_context += f"\nCurrent Follow-up Question: {query}\n"
            
            if is_followup:
                prompt = f"""Based on the following NEW search results (which have been reranked based on your follow-up question) and previous conversation history, provide a comprehensive answer to the follow-up question: "{query}"

{conversation_context}

NEW Search Results (Reranked):
{context}

Please provide:
1. A clear, informative answer that builds on previous context and incorporates new information from the latest search
2. Citations to the sources used (format as [1], [2], etc.) - include both new and relevant previous sources
3. A brief summary of how this new information relates to or expands upon the previous conversation
4. If any sources were excluded, explain why they weren't relevant

Answer:"""
            else:
                prompt = f"""Based on the following search results, provide a comprehensive answer to: "{query}"

{context}

Please provide:
1. A clear, informative answer
2. Citations to the sources used (format as [1], [2], etc.)
3. A brief summary of key findings

Answer:"""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant that provides accurate, well-cited answers based on search results. For follow-up questions, build upon previous context and provide more specific, detailed answers that incorporate new information from the latest search."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return {
                "answer": response.choices[0].message['content'],
                "sources": search_results,
                "excluded_sources": excluded_sources if is_followup else []
            }
        except Exception as e:
            print(f"AI generation error: {e}")
            return {
                "answer": "Sorry, I couldn't generate a response at this time.",
                "sources": search_results,
                "excluded_sources": []
            }

perplexity = PerplexityClone()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/discover")
async def discover(request: Request):
    # Get 3 random topics
    random_topics = random.sample(TOPICS, 3)
    return templates.TemplateResponse("discover.html", {
        "request": request,
        "topics": random_topics
    })

@app.post("/search")
async def search(query: str = Form(...)):
    """Search endpoint that combines web search and AI response"""
    # Clear previous conversation history for new searches
    perplexity.clear_conversation()
    
    # Get search results
    search_results = perplexity.search_web(query)
    
    # Generate AI response
    ai_response = perplexity.generate_ai_response(query, search_results)
    
    # Store in conversation history
    perplexity.conversation_history.append({
        "query": query,
        "answer": ai_response["answer"],
        "sources": ai_response["sources"]
    })
    
    return {
        "query": query,
        "answer": ai_response["answer"],
        "sources": ai_response["sources"],
        "conversation_id": len(perplexity.conversation_history)
    }

@app.post("/followup")
async def followup(query: str = Form(...)):
    """Follow-up search endpoint that uses previous context and performs new search"""
    if not perplexity.conversation_history:
        # If no previous search, perform a regular search
        search_results = perplexity.search_web(query)
        ai_response = perplexity.generate_ai_response(query, search_results)
    else:
        # Get the original query from the first search
        original_query = perplexity.conversation_history[0]["query"]
        
        # Create a combined search query
        combined_query = f"{original_query} {query}"
        
        # Perform new search with combined query
        search_results = perplexity.search_web(combined_query)
        
        # Generate AI response with conversation history
        ai_response = perplexity.generate_ai_response(
            query, 
            search_results, 
            is_followup=True, 
            conversation_history=perplexity.conversation_history
        )
    
    # Store in conversation history
    perplexity.conversation_history.append({
        "query": query,
        "answer": ai_response["answer"],
        "sources": ai_response["sources"]
    })
    
    return {
        "query": query,
        "answer": ai_response["answer"],
        "sources": ai_response["sources"],
        "conversation_id": len(perplexity.conversation_history)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)