# 🕷️ Meraki AI - Your Friendly Neighborhood AI Assistant

> **Real-time voice conversation system with a Spider-Man inspired AI personality**

Meet **Meraki**, your cheerful and witty AI companion with the personality traits of Spider-Man! This sophisticated voice interaction platform combines cutting-edge speech recognition, streaming AI responses, and natural voice synthesis to deliver an engaging conversational experience.

---

## ✨ Key Features

🎯 **Real-time Speech Recognition** - Instant speech-to-text via AssemblyAI streaming  
🧠 **AI-Powered Conversations** - Intelligent streaming responses by Google Gemini  
🔊 **Natural Voice Synthesis** - Human-like speech output via Murf AI WebSocket  
⚡ **WebSocket Streaming** - Ultra-low latency real-time audio processing  
📰 **News Integration** - "Spider-sense" for latest headlines via NewsAPI  
🎭 **Dynamic Personality** - Cheerful Spider-Man inspired AI character  
💬 **Session Memory** - Maintains conversation context across interactions  
🎨 **Modern Interface** - Responsive UI with animated particle effects  
🌐 **RESTful API** - FastAPI backend with comprehensive endpoints  

---

## 🚀 Installation & Setup

### Prerequisites
Ensure you have Python 3.8+ installed, then install dependencies:
```bash
pip install -r requirements.txt
```

### Environment Configuration
Configure your API credentials by creating an environment file:

1. Copy the sample configuration:
   ```bash
   cp .env.sample .env
   ```

2. Add your API keys to the `.env` file:
   ```env
   # Required APIs
   ASSEMBLYAI_API_KEY=your_assemblyai_key_here
   GEMINI_API_KEY=your_gemini_key_here
   MURF_API_KEY=your_murf_key_here
   
   # Optional - for news features
   NEWS_API_KEY=your_news_api_key_here
   ```

### Application Launch
Start the application using the provided launcher:
```bash
python run.py
```

The launcher performs automatic dependency validation and environment checks before starting the server.

### Access the Application
Navigate to: **http://localhost:8000**

---

## 🔧 API Service Configuration

The following services are required for full functionality:

| Service | Purpose | Registration | Required |
|---------|---------|--------------|----------|
| **AssemblyAI** | Real-time speech recognition | [Create Account](https://www.assemblyai.com/) | ✅ Yes |
| **Google Gemini** | AI response generation | [Get API Key](https://ai.google.dev/) | ✅ Yes |
| **Murf AI** | Text-to-speech synthesis | [Sign Up](https://murf.ai/) | ✅ Yes |
| **NewsAPI** | Latest headlines integration | [Register Here](https://newsapi.org/register) | 🔄 Optional |

> **Note**: The application will work without NewsAPI, but Meraki's "spider-sense" news feature will be disabled.

---

## 🏗️ Technical Architecture

The application is built using modern technologies for optimal performance:

- **Backend Framework**: FastAPI with WebSocket support for real-time communication
- **Frontend**: HTML5, CSS3, TailwindCSS, and vanilla JavaScript with particle effects
- **Speech Recognition**: AssemblyAI Streaming API v3 for real-time transcription
- **AI Processing**: Google Gemini 1.5 Flash with streaming responses
- **Voice Synthesis**: Murf AI WebSocket API for low-latency audio generation
- **News Integration**: NewsAPI for real-time headlines
- **Real-time Communication**: WebSocket protocol for bidirectional streaming
- **Session Management**: In-memory chat history with configurable limits
- **Error Handling**: Comprehensive fallback mechanisms and logging

### Project Structure
```
├── app.py                 # Main FastAPI application with WebSocket handlers
├── run.py                 # Application launcher with dependency validation  
├── requirements.txt       # Python dependencies including newsapi-python
├── .env.sample           # Environment template with all API keys
├── templates/
│   └── index.html        # Main UI with Meraki branding and particle effects
└── static/
    └── style.css         # Custom styles and animations
```

---

## 🎯 Usage Instructions

### Basic Interaction
1. **Start Conversation** - Click the animated AI orb to begin recording
2. **Voice Input** - Speak naturally into your microphone
3. **Real-time Feedback** - Watch live transcription appear below the orb
4. **AI Response** - Meraki responds with personality-rich audio
5. **End Recording** - Click the orb again to stop and process

### Special Features

#### 📰 News Integration ("Spider-Sense")
Ask Meraki about current events:
- *"What's in the news?"*
- *"Any headlines today?"*
- *"What's happening in the world?"*

Meraki will use her "spider-sense" to fetch and deliver the latest headlines with characteristic wit!

#### 💭 Conversation Memory
Meraki maintains context throughout your session, remembering previous topics and building on your conversation naturally.

#### 🎭 Adaptive Personality
- **Cheerful & Witty**: Default Spider-Man inspired personality
- **Contextually Serious**: Automatically shifts tone for important topics
- **Conversational**: Uses natural language patterns and humor

---

## 🛠️ Troubleshooting

### Common Issues and Solutions

#### 🚫 **Microphone Access Issues**
- **Browser Permissions**: Ensure microphone access is allowed in browser settings
- **HTTPS Requirement**: Use HTTPS or localhost for microphone API access
- **Hardware Check**: Test microphone in other applications
- **Browser Compatibility**: Use Chrome, Firefox, or Safari (latest versions)

#### 🔑 **API Authentication Errors**
- **Environment File**: Verify `.env` file exists in project root with correct keys
- **API Key Format**: Check for trailing spaces or formatting issues
- **Service Status**: Confirm API accounts are active and have sufficient quotas
- **Key Validation**: Test each API key individually in their respective dashboards

#### 🌐 **Connection & Performance Issues**
- **Port Availability**: Ensure port 8000 is not blocked by firewall
- **Network Stability**: Verify stable internet connection for API calls
- **Resource Usage**: Close unnecessary applications to free system resources
- **Server Restart**: Restart the application using `python run.py`

#### 📰 **News Feature Not Working**
- **API Key Missing**: Check if `NEWS_API_KEY` is set in `.env` file
- **Free Tier Limits**: NewsAPI free tier has daily request limits
- **Network Restrictions**: Some networks may block NewsAPI endpoints

#### 🔊 **Audio Output Problems**
- **Browser Audio**: Check browser audio permissions and system volume
- **Murf API Issues**: Verify Murf API key and account status  
- **Fallback Mode**: Application includes fallback text responses if audio fails
- **WebSocket Connection**: Check browser developer console for WebSocket errors

#### 💬 **AI Response Issues**
- **Gemini API**: Verify Google Gemini API key and quota limits
- **Context Length**: Long conversations may hit context limits (auto-managed)
- **Streaming Errors**: Check network connectivity for streaming responses

### Debug Mode
Enable detailed logging by checking the terminal output when running `python run.py`. Look for:
- ✅ API key validation messages
- 🔍 WebSocket connection status  
- 📝 Request/response logging
- ❌ Error details and stack traces

### Getting Help
1. Check browser developer console (F12) for JavaScript errors
2. Monitor terminal output for backend errors
3. Verify all dependencies: `pip install -r requirements.txt`
4. Test with a fresh virtual environment if issues persist

---

## 📋 System Requirements

### Minimum Requirements
- **Python**: Version 3.8 or higher
- **Browser**: Chrome 80+, Firefox 75+, or Safari 14+ (latest versions recommended)
- **Network**: Stable internet connection (minimum 1 Mbps for real-time features)
- **Hardware**: 
  - Functional microphone and audio output device
  - 2GB RAM (4GB recommended for optimal performance)
  - Modern CPU for real-time audio processing

### Recommended Setup
- **OS**: Windows 10/11, macOS 10.15+, or Ubuntu 18.04+
- **Python**: Version 3.9+ with virtual environment
- **RAM**: 4GB+ for smooth streaming performance  
- **Network**: Broadband connection for best real-time experience

---

## 🎭 Meet Meraki

**Meraki** is your friendly neighborhood AI assistant with a unique personality inspired by Spider-Man. Here's what makes her special:

### Personality Traits
- **Cheerful & Optimistic**: Always looking on the bright side
- **Witty & Humorous**: Delivers clever jokes and lighthearted banter
- **Contextually Aware**: Knows when to be serious about important matters
- **Conversational**: Engages in natural, flowing dialogue
- **News-Savvy**: Uses her "spider-sense" to stay updated on current events

### Interaction Style
- Greets with casual phrases like *"What's up, doc?"*
- Maintains Spider-Man's friendly neighborhood vibe
- Adapts tone based on conversation context
- Provides concise, natural responses optimized for voice interaction

---

## 🚀 Development & Customization

### Key Components
- **`app.py`**: Main application with WebSocket handlers and API endpoints
- **`run.py`**: Startup script with dependency validation
- **`templates/index.html`**: Frontend interface with Meraki branding
- **`static/style.css`**: Custom animations and particle effects

### Personality Customization
Modify the `AI_SYSTEM_PROMPT` in `app.py` to adjust Meraki's personality, greeting style, and response patterns.

### Adding New Features
The modular architecture makes it easy to extend functionality:
- Add new API integrations following the existing pattern
- Implement additional WebSocket endpoints for real-time features
- Customize the UI with new animations and styles

---

## 📄 License & Credits

This project demonstrates modern AI voice interaction capabilities using cutting-edge APIs and technologies. Built with love for the AI community! 🕷️✨


