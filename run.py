#!/usr/bin/env python3
"""
Startup script for the Murf AI Voice Agent
Simple launcher with dependency validation
"""

import os
import sys
import subprocess

def check_dependencies():
    """Check if all required packages are installed"""
    try:
        import fastapi
        import uvicorn
        import assemblyai
        import google.generativeai
        import requests
        import websockets
        import aiohttp
        import newsapi
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def main():
    """Main startup function"""
    print("🚀 Starting Murf AI Voice Agent...")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Start the server
    print("🌟 Starting server...")
    print("📡 Server will be available at: http://127.0.0.1:8000")
    print("🔑 Please configure your API keys in the UI before starting.")
    print("-" * 50)
    
    try:
        # Run the main FastAPI application
        import uvicorn
        port = int(os.environ.get("PORT", 8000))
        host = "0.0.0.0" if os.environ.get("RENDER") else "127.0.0.1"
        uvicorn.run(
            "app:app",
            host=host,
            port=port,
            reload=False if os.environ.get("RENDER") else True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Goodbye! Server stopped.")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

