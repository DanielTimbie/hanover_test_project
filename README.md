# AI-Powered Search & Discovery Platform

A modern search platform that combines web search with AI-powered answers, inspired by Perplexity. This application provides intelligent search capabilities with follow-up questions, source reranking, and topic discovery.

## Features

### 🔍 Smart Search
- Ask any question and get comprehensive, AI-generated answers
- Results include relevant web sources with snippets and citations
- Clean, modern interface with real-time response generation

### 💬 Interactive Follow-ups
- Ask follow-up questions about your search results
- The system maintains conversation context
- Each follow-up can build upon previous answers while bringing in new information

### 🔄 Dynamic Source Reranking
- Control your sources through natural language
- Examples:
  - "Show me the same info but exclude Quora sources"
  - "Only show academic sources"
  - "Prioritize recent articles"
- Sources can be excluded or reordered based on your preferences
- Clear explanations for why sources were included or excluded

### 🎯 Topic Discovery
- Explore curated topics across multiple categories:
  - Technology
  - Science
  - Health & Wellness
  - Culture & Society
  - Emerging Fields
- Click any category to see 5 random topics
- Use the shuffle button to get different topic suggestions
- Topics automatically populate the search bar (but don't auto-search)

## How to Use

### Basic Search
1. Type your question in the main search bar
2. Click "Search" or press Enter
3. View the AI-generated answer with cited sources

### Follow-up Questions
1. After getting search results, use the follow-up input box below
2. Ask for clarification, more details, or related information
3. The system will maintain context from your previous search

### Source Control
- In your follow-up questions, you can control sources:
  ```
  "Can you explain this again without using Reddit sources?"
  "Show me only results from educational websites"
  "Focus on the most recent sources"
  ```
- The system will rerank and filter sources accordingly
- Excluded sources are shown separately with explanations

### Topic Discovery
1. Click any category button to see topic suggestions
2. Click a topic to populate it in the search bar
3. Click "Search" when ready to explore that topic
4. Use the shuffle button to see different topics within the category

## Examples

### Sample Conversation Flow
1. Initial search: "What are the latest developments in quantum computing?"
2. Follow-up: "Focus on practical applications"
3. Follow-up: "Show me only results from research institutions"

### Topic Exploration
1. Click "Technology" category
2. Select "AI Ethics" from suggestions
3. Search and explore
4. Ask follow-up questions to dive deeper

## Tips
- Be specific in your questions for better results
- Use follow-ups to refine and focus your search
- Experiment with source preferences in follow-up questions
- Try different categories to discover interesting topics
- Use the shuffle feature to explore more options within each category

## Technical Requirements
- Modern web browser
- Internet connection
- API keys (for deployment)

## Getting Started
1. Clone the repository
2. Install dependencies
3. Set up environment variables
4. Run the application

For detailed setup instructions, see the installation guide. 