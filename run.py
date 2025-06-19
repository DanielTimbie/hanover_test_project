#!/usr/bin/env python3
"""
Simple runner script for the Perplexity Clone
"""
import uvicorn

if __name__ == "__main__":
    print("🚀 Starting Perplexity Clone...")
    print("📱 Open http://localhost:8000 in your browser")
    print("⏹️  Press Ctrl+C to stop")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True) 