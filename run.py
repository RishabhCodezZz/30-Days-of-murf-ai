#!/usr/bin/env python3
"""
Startup script for the Murf AI Voice Agent
Simple launcher with dependency and environment validation
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if all required packages are installed"""
    try:
        import fastapi
        import uvicorn
        import assemblyai
        import google.generativeai
        import requests
        from dotenv import load_dotenv
        import websockets
        import aiohttp
        # --- NEW: Also check for newsapi client ---
        import newsapi
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Run: pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if .env file exists and has required keys"""
    env_path = Path('.env')
    if not env_path.exists():
        print("❌ .env file not found")
        print("Please create a .env file with your API keys:")
        print("ASSEMBLYAI_API_KEY=your_key_here")
        print("GEMINI_API_KEY=your_key_here")
        print("MURF_API_KEY=your_key_here")
        # --- NEW: Add News API key to the instructions ---
        print("NEWS_API_KEY=your_key_here")
        return False
    
    # Check if keys are present
    from dotenv import load_dotenv
    load_dotenv()
    
    # --- MODIFIED: Add NEWS_API_KEY to the list of required keys ---
    required_keys = ["ASSEMBLYAI_API_KEY", "GEMINI_API_KEY", "MURF_API_KEY", "NEWS_API_KEY"]
    missing_keys = []
    
    for key in required_keys:
        if not os.getenv(key):
            missing_keys.append(key)
    
    if missing_keys:
        print(f"❌ Missing API keys in .env: {', '.join(missing_keys)}")
        return False
    
    print("✅ Environment variables configured")
    return True

def main():
    """Main startup function"""
    print("🚀 Starting Murf AI Voice Agent...")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check environment
    if not check_env_file():
        sys.exit(1)
    
    # Start the server
    print("🌟 Starting server with advanced features...")
    print("📡 Server will be available at: http://127.0.0.1:8000")
    print("🎤 Features enabled:")
    print("   • Real-time speech recognition (AssemblyAI)")
    print("   • AI-powered responses (Google Gemini)")
    print("   • Voice synthesis (Murf)")
    print("   • WebSocket streaming")
    # --- NEW: Add news skill to the feature list ---
    print("   • 'Spider-Sense' for News (NewsAPI)")
    print("   • Modern UI interface")
    print("-" * 50)
    print("🎵 Audio Processing:")
    print("   • Real-time speech-to-text transcription")
    print("   • AI response generation and voice synthesis")
    print("   • Automatic error handling with fallbacks")
    print("-" * 50)
    
    try:
        # Run the main FastAPI application
        import app
        import uvicorn
        uvicorn.run(
            "app:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Goodbye! Server stopped.")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
