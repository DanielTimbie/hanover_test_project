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

load_dotenv()

app = FastAPI(title="Perplexity Clone", version="1.0.0")
templates = Jinja2Templates(directory="templates")

# Configure APIs
openai.api_key = os.getenv("OPENAI_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

class PerplexityClone:
    def __init__(self):
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
    
    def generate_ai_response(self, query: str, search_results: List[Dict]) -> Dict:
        """Generate AI response based on search results"""
        try:
            # Format search results for AI context
            context = "Search Results:\n"
            for i, result in enumerate(search_results, 1):
                context += f"{i}. {result['title']}\n"
                context += f"   {result['snippet']}\n"
                context += f"   Source: {result['link']}\n\n"
            
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
                    {"role": "system", "content": "You are a helpful AI assistant that provides accurate, well-cited answers based on search results."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return {
                "answer": response.choices[0].message.content,
                "sources": search_results
            }
        except Exception as e:
            print(f"AI generation error: {e}")
            return {
                "answer": "Sorry, I couldn't generate a response at this time.",
                "sources": search_results
            }

perplexity = PerplexityClone()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/search")
async def search(query: str = Form(...)):
    """Search endpoint that combines web search and AI response"""
    # Get search results
    search_results = perplexity.search_web(query)
    
    # Generate AI response
    ai_response = perplexity.generate_ai_response(query, search_results)
    
    return {
        "query": query,
        "answer": ai_response["answer"],
        "sources": ai_response["sources"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 