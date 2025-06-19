# Perplexity Clone

A simple web app that combines search results with AI-generated answers, similar to Perplexity AI.

## What it does

- Takes user queries and searches the web using SerpAPI
- Generates AI responses based on the search results using OpenAI
- Displays answers with citations to the original sources
- Clean, simple web interface

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file with your API keys:
```
OPENAI_API_KEY=your_key_here
SERPAPI_KEY=your_key_here
```

3. Run the app:
```bash
python run.py
```

Visit `http://localhost:8000` to use it.

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML/CSS/JS
- **APIs**: OpenAI GPT-3.5, SerpAPI
- **Styling**: Custom CSS with modern design

## Files

- `main.py` - FastAPI app with search and AI endpoints
- `templates/index.html` - Web interface
- `requirements.txt` - Python dependencies

The app demonstrates basic API integration, error handling, and a clean user experience. 