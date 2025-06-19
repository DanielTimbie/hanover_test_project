# Perplexity Clone - 2-Hour Assessment

A Python-based clone of Perplexity AI that combines web search results with AI-generated responses and citations.

## Features

- **Web Search Integration**: Uses SerpAPI to fetch real-time search results
- **AI Response Generation**: OpenAI GPT-3.5-turbo for intelligent answers
- **Citation System**: Automatic source attribution and formatting
- **Modern UI**: Clean, responsive interface with loading states
- **Error Handling**: Graceful fallbacks for API failures

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up API Keys
Create a `.env` file with your API keys:
```bash
cp env_example.txt .env
# Edit .env with your actual API keys
```

Required APIs:
- **OpenAI API**: For AI response generation
- **SerpAPI**: For web search results

### 3. Run the Application
```bash
python main.py
```

Visit `http://localhost:8000` in your browser.

## Architecture

### Core Components

1. **FastAPI Backend** (`main.py`)
   - RESTful API endpoints
   - Search and AI response orchestration
   - Error handling and validation

2. **PerplexityClone Class**
   - `search_web()`: SerpAPI integration
   - `generate_ai_response()`: OpenAI integration with context

3. **Frontend** (`templates/index.html`)
   - Modern, responsive UI
   - Real-time search and results display
   - Citation formatting

### API Endpoints

- `GET /`: Main application interface
- `POST /search`: Search endpoint (query → search results + AI response)

## Technical Decisions

### Why This Stack?
- **FastAPI**: Rapid development, automatic API docs, async support
- **SerpAPI**: Reliable search results with structured data
- **OpenAI GPT-3.5**: Cost-effective, reliable AI responses
- **Vanilla JS**: No build process, immediate deployment

### Performance Optimizations
- Limited search results (5) for faster response
- Efficient prompt engineering for AI context
- Client-side result formatting
- Graceful error handling

## Assessment Strategy

### Time Allocation (2 Hours)
1. **Setup & Foundation** (20 min): Project structure, dependencies
2. **Core Functionality** (60 min): Search + AI integration
3. **Enhancement** (40 min): UI polish, error handling

### Key Demonstrations
- **API Integration**: Multiple external services
- **Error Handling**: Graceful failures
- **User Experience**: Loading states, clean UI
- **Code Quality**: Clean architecture, documentation

## Future Enhancements

Given more time:
- **Caching**: Redis for search results
- **Rate Limiting**: API usage optimization
- **Advanced Search**: Filters, date ranges
- **User Sessions**: Query history
- **Analytics**: Usage tracking
- **Testing**: Unit and integration tests

## API Setup

### OpenAI
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Create account and get API key
3. Add to `.env`: `OPENAI_API_KEY=sk-...`

### SerpAPI
1. Visit [SerpAPI](https://serpapi.com/)
2. Sign up for free tier (100 searches/month)
3. Add to `.env`: `SERPAPI_KEY=...` 