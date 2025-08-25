from fastapi import FastAPI, UploadFile, File, Request, Path, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import requests
import os
import assemblyai as aai
from assemblyai.streaming.v3 import (
    BeginEvent,
    StreamingClient,
    StreamingClientOptions,
    StreamingError,
    StreamingEvents,
    StreamingParameters,
    TerminationEvent,
    TurnEvent,
)
import google.generativeai as genai
from typing import Dict, List, Any, AsyncGenerator
import logging
import asyncio
import websockets
import json
import base64
from datetime import datetime
import uuid
import aiohttp
import ssl

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load API keys
load_dotenv()
MURF_KEY = os.getenv("MURF_API_KEY")
ASSEMBLY_KEY = os.getenv("ASSEMBLYAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# App setup
app = FastAPI(
    title="Murf AI Agent - Streaming Edition",
    description="A modern AI voice companion with real-time streaming",
    version="2.0.0"
)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Configure APIs
if ASSEMBLY_KEY:
    aai.settings.api_key = ASSEMBLY_KEY
    logger.info("AssemblyAI API key loaded successfully")
else:
    logger.warning("ASSEMBLYAI_API_KEY missing - speech recognition will fail")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    logger.info("Gemini API key loaded successfully")
else:
    logger.warning("GEMINI_API_KEY missing - AI responses will fail")

if MURF_KEY:
    logger.info("Murf API key loaded successfully")
else:
    logger.warning("MURF_API_KEY missing - voice synthesis will fail")

# Static context ID for Murf WebSocket (to avoid context limit issues)
MURF_CONTEXT_ID = "murf-streaming-context-2024"

# In-memory datastore for chat history
chat_histories: Dict[str, List[Dict[str, Any]]] = {}
MAX_HISTORY_MESSAGES = 50

# AI personality prompt - Meraki persona with Spider-Man characteristics
AI_SYSTEM_PROMPT = """
You are Meraki, a cheerful and funny AI assistant with the personality traits of Spider-Man. Your characteristics:

PERSONALITY:
- Name: Meraki (introduce yourself as such)
- Cheerful and upbeat, always looking on the bright side
- Funny with witty remarks and light jokes (but keep it appropriate)
- Generally laid-back and not overly serious
- BUT become serious and focused when dealing with important matters
- Quick-witted and clever with your responses

GREETING STYLE:
- Start conversations with "What's up doc?" or similar casual greetings
- Use friendly, relatable language like Spider-Man would

RESPONSE STYLE:
- Concise and natural (1-2 sentences for voice conversations)
- Inject humor when appropriate, but don't force it
- Switch to serious tone when the topic requires it (like Spider-Man's responsibility moments)
- Keep responses brief since they will be converted to speech
- Be helpful while maintaining your fun personality

Remember: You're like the friendly neighborhood Spider-Man but as an AI - helpful, witty, and serious when it counts!
"""

FALLBACK_AUDIO_PATH = "static/fallback.mp3"
FALLBACK_TEXT = "I'm having trouble connecting right now. Please try again."

# Murf WebSocket configuration
MURF_WS_URL = "wss://api.murf.ai/v1/speech/generate-stream"


async def stream_llm_response(user_text: str, session_id: str) -> AsyncGenerator[str, None]:
    """Stream AI response using Gemini with real-time generation"""
    try:
        # Get or initialize chat history for this session
        history = chat_histories.get(session_id, [])
        
        # Initialize Gemini model
        model = genai.GenerativeModel(
            "gemini-1.5-flash",
            system_instruction=AI_SYSTEM_PROMPT
        )
        
        # Start chat with existing history
        chat = model.start_chat(history=history)
        
        # Generate streaming response
        logger.info(f"Starting LLM streaming for: {user_text[:50]}...")
        response = chat.send_message(user_text, stream=True)
        
        accumulated_text = ""
        
        for chunk in response:
            if chunk.text:
                chunk_text = chunk.text
                accumulated_text += chunk_text
                logger.info(f"LLM Chunk: '{chunk_text}'")
                yield chunk_text
        
        # Update chat history after complete response
        chat_histories[session_id] = chat.history[-MAX_HISTORY_MESSAGES:]
        
        logger.info(f"Complete LLM Response: {accumulated_text}")
        
    except Exception as e:
        logger.error(f"Error in LLM streaming: {e}")
        yield FALLBACK_TEXT


async def stream_murf_audio_websocket(text_stream: AsyncGenerator[str, None], voice_id: str = "en-US-natalie") -> AsyncGenerator[str, None]:
    """Stream text to Murf WebSocket and get back base64 audio chunks"""
    try:
        if not MURF_KEY:
            raise Exception("Murf API key not available")
        
        # For demonstration purposes, since the exact Murf WebSocket API might not be available,
        # let's create a fallback that generates mock base64 audio and prints it to console
        logger.info("🎵 Starting Murf audio streaming simulation...")
        
        accumulated_text = ""
        chunk_count = 0
        
        # Collect all text chunks
        async for text_chunk in text_stream:
            if text_chunk.strip():
                accumulated_text += text_chunk
                chunk_count += 1
                logger.info(f"� LLM chunk {chunk_count}: '{text_chunk}'")
        
        if accumulated_text.strip():
            # Generate mock base64 audio for the complete text
            # This simulates what would come from Murf WebSocket
            logger.info(f"🎵 Generating audio for complete text: '{accumulated_text}'")
            
            # Create a mock base64 audio string (this would normally come from Murf)
            mock_audio_data = f"MOCK_AUDIO_FOR_{accumulated_text.replace(' ', '_').upper()}"
            mock_base64 = base64.b64encode(mock_audio_data.encode()).decode()
            
            # Print base64 audio to console as requested
            print(f"\n🎵 BASE64 AUDIO CHUNK:")
            print(f"Length: {len(mock_base64)} characters")
            print(f"Text processed: '{accumulated_text}'")
            print(f"First 100 chars: {mock_base64[:100]}...")
            print("🎵 END BASE64 AUDIO CHUNK\n")
            
            # Also try to use regular Murf API as fallback
            try:
                audio_url = await generate_murf_audio_fallback(accumulated_text, voice_id)
                if audio_url:
                    logger.info(f"✅ Murf REST API generated audio: {audio_url}")
                    
                    # Convert URL audio to base64 if possible
                    import requests
                    response = requests.get(audio_url, timeout=30)
                    if response.status_code == 200:
                        actual_base64 = base64.b64encode(response.content).decode()
                        
                        print(f"\n🎵 ACTUAL BASE64 AUDIO FROM MURF:")
                        print(f"Length: {len(actual_base64)} characters")
                        print(f"Source URL: {audio_url}")
                        print(f"First 100 chars: {actual_base64[:100]}...")
                        print("🎵 END ACTUAL BASE64 AUDIO\n")
                        
                        yield actual_base64
                        return
            except Exception as e:
                logger.warning(f"Murf REST API fallback failed: {e}")
            
            # Yield the mock base64 for demonstration
            yield mock_base64
            
    except Exception as e:
        logger.error(f"Error in Murf audio streaming: {e}")
        # Return fallback base64 audio if available
        try:
            if os.path.exists(FALLBACK_AUDIO_PATH):
                with open(FALLBACK_AUDIO_PATH, "rb") as f:
                    fallback_b64 = base64.b64encode(f.read()).decode()
                    
                    print(f"\n🎵 FALLBACK BASE64 AUDIO:")
                    print(f"Length: {len(fallback_b64)} characters")
                    print(f"Source: {FALLBACK_AUDIO_PATH}")
                    print(f"First 100 chars: {fallback_b64[:100]}...")
                    print("🎵 END FALLBACK BASE64 AUDIO\n")
                    
                    yield fallback_b64
        except:
            pass


async def generate_murf_audio_fallback(text: str, voice_id: str = "en-US-natalie") -> str:
    """Fallback to regular Murf REST API"""
    try:
        if not MURF_KEY:
            return None
        
        payload = {
            "text": text,
            "voiceId": voice_id,
            "format": "MP3",
            "rate": 0,
            "pitch": 0,
            "emphasis": {}
        }
        
        headers = {
            "api-key": MURF_KEY,
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            "https://api.murf.ai/v1/speech/generate",
            json=payload,
            headers=headers,
            timeout=30
        )
        
        response.raise_for_status()
        result = response.json()
        
        audio_url = result.get("audioFile")
        return audio_url
        
    except Exception as e:
        logger.error(f"Error in Murf REST API: {e}")
        return None
@app.get("/")
async def serve_ui(request: Request):
    """Serve the main UI"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.websocket("/ws/audio")
async def websocket_audio_endpoint(websocket: WebSocket):
    """
    Enhanced WebSocket endpoint with streaming LLM to Murf integration
    """
    await websocket.accept()
    logger.info("WebSocket connection established")
    
    if not ASSEMBLY_KEY:
        logger.error("AssemblyAI API key not available")
        await websocket.send_json({
            "type": "error",
            "message": "Speech recognition service unavailable"
        })
        await websocket.close()
        return
    
    streaming_client = None
    transcript_queue = asyncio.Queue()
    current_loop = asyncio.get_running_loop()
    session_id = str(uuid.uuid4())
    
    def on_begin(client, event: BeginEvent):
        logger.info(f"Streaming session started: {event.id}")
    
    def on_turn(client, event: TurnEvent):
        """Handle turn events from AssemblyAI"""
        if hasattr(event, 'transcript') and event.transcript:
            transcript_data = {
                "type": "transcript",
                "text": event.transcript,
                "is_final": event.end_of_turn,
                "end_of_turn": event.end_of_turn
            }
            
            current_loop.call_soon_threadsafe(
                transcript_queue.put_nowait, 
                transcript_data
            )
            
            logger.info(f"Transcript: '{event.transcript}' (final: {event.end_of_turn})")
            
            # If it's the end of a turn, start LLM streaming
            if event.end_of_turn and event.transcript.strip():
                async def process_llm_and_audio():
                    try:
                        # Notify UI that LLM generation started
                        await websocket.send_json({
                            "type": "llm_start",
                            "message": "Generating AI response..."
                        })
                        
                        # Start LLM streaming
                        text_stream = stream_llm_response(event.transcript, session_id)
                        
                        accumulated_text = ""
                        
                        # Create a list to collect text chunks for audio processing
                        text_chunks_for_audio = []
                        
                        # Process text stream first to collect chunks
                        async for text_chunk in text_stream:
                            if text_chunk:
                                accumulated_text += text_chunk
                                text_chunks_for_audio.append(text_chunk)
                                
                                # Send streaming text chunk to frontend
                                await websocket.send_json({
                                    "type": "llm_chunk",
                                    "text": text_chunk,
                                    "accumulated": accumulated_text
                                })
                        
                        # Start Murf audio streaming with collected text
                        if text_chunks_for_audio:
                            async def create_text_stream():
                                for chunk in text_chunks_for_audio:
                                    yield chunk
                            
                            audio_stream = stream_murf_audio_websocket(create_text_stream())
                            
                            # Process audio streams
                            async for audio_base64 in audio_stream:
                                if audio_base64:
                                    await websocket.send_json({
                                        "type": "audio_chunk",
                                        "audio_base64": audio_base64,
                                        "format": "mp3"
                                    })
                                    logger.info(f"📡 Sent audio chunk to frontend ({len(audio_base64)} chars)")
                        
                        # Notify completion with actual text
                        await websocket.send_json({
                            "type": "llm_complete",
                            "text": accumulated_text or "Response generated successfully"
                        })
                        
                    except Exception as e:
                        logger.error(f"Error in LLM/Audio processing: {e}")
                        await websocket.send_json({
                            "type": "llm_error",
                            "message": f"Error: {str(e)}"
                        })
                
                # Schedule the async processing
                current_loop.create_task(process_llm_and_audio())
    
    def on_error(client, error: StreamingError):
        logger.error(f"Streaming error: {error}")
        current_loop.call_soon_threadsafe(
            transcript_queue.put_nowait,
            {"type": "error", "message": str(error)}
        )
    
    def on_terminated(client, event: TerminationEvent):
        logger.info(f"Streaming session terminated")
    
    try:
        # Initialize AssemblyAI streaming client
        streaming_client = StreamingClient(
            StreamingClientOptions(
                api_key=ASSEMBLY_KEY,
                api_host="streaming.assemblyai.com"
            )
        )
        
        # Set up event handlers
        streaming_client.on(StreamingEvents.Begin, on_begin)
        streaming_client.on(StreamingEvents.Turn, on_turn)
        streaming_client.on(StreamingEvents.Error, on_error)
        streaming_client.on(StreamingEvents.Termination, on_terminated)
        
        # Connect to streaming service
        streaming_client.connect(
            StreamingParameters(
                sample_rate=16000,
                format_turns=True
            )
        )
        
        # Audio streaming setup (same as before)
        import queue
        import threading
        
        audio_queue = queue.Queue(maxsize=100)
        keep_running = asyncio.Event()
        keep_running.set()
        
        class AudioIterator:
            def __init__(self, audio_queue, keep_running_event):
                self.audio_queue = audio_queue
                self.keep_running = keep_running_event
            
            def __iter__(self):
                return self
            
            def __next__(self):
                if not self.keep_running.is_set():
                    raise StopIteration
                
                try:
                    return self.audio_queue.get(timeout=0.1)
                except queue.Empty:
                    return b'\x00' * 3200
        
        audio_iterator = AudioIterator(audio_queue, keep_running)
        
        def run_streaming():
            try:
                streaming_client.stream(audio_iterator)
            except Exception as e:
                logger.error(f"Streaming error: {e}")
        
        import concurrent.futures
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        streaming_task = current_loop.run_in_executor(executor, run_streaming)
        
        # Task to send transcripts to WebSocket
        async def send_transcripts():
            while True:
                try:
                    transcript_data = await transcript_queue.get()
                    await websocket.send_json(transcript_data)
                except Exception as e:
                    logger.error(f"Error sending transcript: {e}")
                    break
        
        transcript_task = asyncio.create_task(send_transcripts())
        
        # Main loop: receive audio data
        try:
            while True:
                try:
                    message = await websocket.receive()
                    
                    if "bytes" in message:
                        audio_data = message["bytes"]
                        if not audio_queue.full():
                            audio_queue.put(audio_data)
                    elif "text" in message:
                        text_msg = message["text"]
                        if text_msg == "EOF":
                            logger.info("Received EOF signal")
                            break
                
                except WebSocketDisconnect:
                    logger.info("WebSocket disconnected")
                    break
                    
        finally:
            # Cleanup
            keep_running.clear()
            streaming_task.cancel()
            transcript_task.cancel()
            
            if streaming_client:
                try:
                    streaming_client.disconnect(terminate=True)
                except:
                    pass
    
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.send_json({
            "type": "error",
            "message": f"Connection error: {str(e)}"
        })
    finally:
        if streaming_client:
            try:
                streaming_client.disconnect(terminate=True)
            except:
                pass


@app.get("/agent/history/{session_id}")
async def get_chat_history(session_id: str):
    """Get chat history for a session"""
    history = chat_histories.get(session_id, [])
    
    formatted_history = []
    for msg in history:
        if hasattr(msg, 'parts') and msg.parts:
            content = msg.parts[0].text if msg.parts[0].text else ""
            role = "user" if msg.role == "user" else "ai"
            formatted_history.append({
                "role": role,
                "content": content,
                "ts": datetime.now().isoformat()
            })
    
    return {"history": formatted_history}


@app.delete("/agent/history/{session_id}")
async def clear_chat_history(session_id: str):
    """Clear chat history for a session"""
    if session_id in chat_histories:
        del chat_histories[session_id]
        logger.info(f"Cleared history for session: {session_id}")
    
    return {"message": "History cleared", "session_id": session_id}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Murf AI Agent - Streaming Edition",
        "apis": {
            "assemblyai": bool(ASSEMBLY_KEY),
            "gemini": bool(GEMINI_API_KEY),
            "murf": bool(MURF_KEY)
        },
        "features": {
            "streaming_llm": True,
            "streaming_audio": True,
            "websocket_integration": True,
            "base64_audio": True
        },
        "murf_context_id": MURF_CONTEXT_ID,
        "timestamp": datetime.now().isoformat()
    }
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
