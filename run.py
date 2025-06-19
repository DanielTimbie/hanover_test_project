#!/usr/bin/env python3
"""
Simple runner script for the Perplexity Clone
"""
import uvicorn
from main import app

if __name__ == "__main__":
    print("🚀 Starting Perplexity Clone...")
    print("📱 Open http://localhost:8000 in your browser")
    print("⏹️  Press Ctrl+C to stop")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True) 