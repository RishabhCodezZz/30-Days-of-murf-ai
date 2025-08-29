# Meraki AI - Voice Assistant

> **A sophisticated real-time voice conversation system powered by cutting-edge AI technologies**

Meraki AI is an intelligent voice assistant that combines advanced speech recognition, streaming AI responses, and natural voice synthesis to create engaging conversational experiences. Built with modern web technologies and powered by industry-leading APIs, it offers seamless voice interactions with a friendly AI personality.

## 🌟 Key Features

### Core Capabilities
- **🎤 Real-Time Speech Recognition** - Instant speech-to-text conversion using AssemblyAI's streaming API
- **🧠 Intelligent AI Conversations** - Dynamic responses powered by Google Gemini with streaming capabilities
- **🔊 Natural Voice Synthesis** - Human-like speech output through Murf AI's advanced text-to-speech
- **📰 News Integration** - Stay updated with current headlines via NewsAPI integration
- **💭 Session Memory** - Maintains conversation context throughout your interaction
- **🎨 Modern Interface** - Responsive web UI with smooth animations and particle effects

### User Experience
- **One-Click Interaction** - Simply click the animated orb to start conversations
- **Live Transcription** - See your words transcribed in real-time as you speak
- **Contextual Responses** - AI remembers previous parts of your conversation
- **Multi-Modal Feedback** - Visual, audio, and text feedback for comprehensive interaction

## 🚀 Quick Start Guide

### Prerequisites
Ensure you have Python 3.8 or higher installed on your system. You can check your Python version by running:
```bash
python --version
```

### Installation Steps

1. **Clone or Download the Project**
   ```bash
   # If using git
   git clone <repository-url>
   cd meraki-ai
   
   # Or download and extract the ZIP file
   ```

2. **Install Required Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   This will install all necessary Python packages including FastAPI, WebSocket support, and API clients.

3. **Launch the Application**
   ```bash
   python run.py
   ```
   The launcher will automatically validate dependencies and start the server.

4. **Access the Web Interface**
   - Open your web browser
   - Navigate to: `http://localhost:8000`
   - You should see the Meraki AI interface with an animated orb

5. **Configure API Keys**
   - Click the "Settings" button in the top-right corner
   - Enter your API keys in the configuration modal
   - Click "Save Keys" to store your credentials

6. **Start Your First Conversation**
   - Click the central animated orb to begin recording
   - Speak naturally into your microphone
   - Watch as your speech is transcribed in real-time
   - Listen to Meraki's AI-generated response
   - Click the orb again to stop recording

## 🔑 API Configuration

Meraki AI requires API keys from several services to function properly. All services offer free tiers suitable for testing and personal use.

### Required Services

| Service | Purpose | Free Tier | Registration Link |
|---------|---------|-----------|-------------------|
| **AssemblyAI** | Speech Recognition | ✅ 5 hours/month | [Sign Up](https://www.assemblyai.com/) |
| **Google Gemini** | AI Responses | ✅ Generous limits | [Get API Key](https://ai.google.dev/) |
| **Murf AI** | Text-to-Speech | ✅ Limited usage | [Create Account](https://murf.ai/) |
| **NewsAPI** | Headlines (Optional) | ✅ 1000 requests/day | [Register](https://newsapi.org/) |

### API Key Setup Process

1. **AssemblyAI Setup**
   - Visit [AssemblyAI](https://www.assemblyai.com/)
   - Create a free account
   - Navigate to your dashboard
   - Copy your API key from the account settings

2. **Google Gemini Setup**
   - Go to [Google AI Studio](https://ai.google.dev/)
   - Sign in with your Google account
   - Create a new API key
   - Copy the generated key

3. **Murf AI Setup**
   - Register at [Murf AI](https://murf.ai/)
   - Complete account verification
   - Access your API credentials in account settings
   - Copy your API key

4. **NewsAPI Setup (Optional)**
   - Visit [NewsAPI](https://newsapi.org/)
   - Register for a free developer account
   - Verify your email address
   - Copy your API key from the dashboard

### Entering API Keys
Once you have your API keys:
1. Open the Meraki AI web interface
2. Click the "Settings" gear icon in the top-right
3. Enter each API key in the corresponding field
4. Click "Save Keys" to store them securely
5. The keys are saved locally in your browser

## 💬 How to Use Meraki AI

### Basic Conversation Flow

1. **Initiate Recording**
   - Click the animated orb in the center of the screen
   - The orb will change color to indicate it's listening
   - Grant microphone permissions if prompted by your browser

2. **Speak Naturally**
   - Talk normally into your microphone
   - You'll see live transcription appear below the orb
   - Speak clearly for best recognition accuracy

3. **AI Processing**
   - When you finish speaking, click the orb again to stop recording
   - The orb will show a processing animation
   - Meraki AI generates a contextual response

4. **Listen to Response**
   - The AI response is played back through your speakers
   - The orb animates during speech playback
   - Text of the conversation appears in the chat history

### Special Features

#### News Integration
Ask Meraki about current events using phrases like:
- "What's in the news today?"
- "Any interesting headlines?"
- "Tell me about current events"
- "What's happening in the world?"

#### Conversation Memory
Meraki remembers your conversation context, so you can:
- Reference previous topics
- Ask follow-up questions
- Build on earlier discussions
- Maintain natural conversation flow

#### Chat History
- View your conversation history in the expandable chat panel
- Clear history using the "Clear" button
- History persists during your session

## 🛠️ Technical Architecture

### Technology Stack
- **Backend Framework**: FastAPI with WebSocket support for real-time communication
- **Frontend**: Modern HTML5, CSS3, and vanilla JavaScript
- **Speech Processing**: AssemblyAI Streaming API v3 for real-time transcription
- **AI Engine**: Google Gemini 1.5 Flash with streaming response generation
- **Voice Synthesis**: Murf AI WebSocket API for low-latency audio generation
- **News Service**: NewsAPI for real-time headline integration
- **Communication**: WebSocket protocol for bidirectional streaming

### Project Structure
```
meraki-ai/
├── app.py                 # Main FastAPI application with WebSocket handlers
├── run.py                 # Application launcher with dependency validation
├── requirements.txt       # Python package dependencies
├── templates/
│   └── index.html        # Main web interface with Meraki branding
└── static/
    └── style.css         # Custom styles and animations
```

## 📋 System Requirements

### Minimum Requirements
- **Operating System**: Windows 10+, macOS 10.15+, or Linux (Ubuntu 18.04+)
- **Python**: Version 3.8 or higher
- **RAM**: 2GB available memory
- **Storage**: 100MB free disk space
- **Network**: Stable internet connection (minimum 1 Mbps)

### Browser Compatibility
- **Chrome**: Version 80+ (Recommended)
- **Firefox**: Version 75+
- **Safari**: Version 14+
- **Edge**: Version 80+

### Hardware Requirements
- **Microphone**: Any functional microphone (built-in or external)
- **Speakers/Headphones**: For audio output
- **CPU**: Modern processor capable of real-time audio processing

## 🔧 Troubleshooting Guide

### Common Issues and Solutions

#### Microphone Access Problems
**Issue**: Browser doesn't detect microphone or access is denied
**Solutions**:
- Ensure you're accessing the site via `https://` or `localhost`
- Check browser permissions: Settings → Privacy → Microphone
- Test microphone in other applications to verify it's working
- Try refreshing the page and granting permissions again
- Use Chrome or Firefox for best compatibility

#### API Authentication Errors
**Issue**: "API key invalid" or authentication failures
**Solutions**:
- Verify all API keys are entered correctly (no extra spaces)
- Check that your API accounts are active and verified
- Ensure you haven't exceeded free tier limits
- Test each API key individually in their respective dashboards
- Re-enter keys if you suspect they were corrupted

#### Audio Playback Issues
**Issue**: Can't hear AI responses or audio is distorted
**Solutions**:
- Check system volume and browser audio settings
- Verify speakers/headphones are connected and working
- Test audio in other applications
- Try different browsers
- Check if browser has audio permissions for the site

#### Connection and Performance Issues
**Issue**: Slow responses, timeouts, or connection errors
**Solutions**:
- Check your internet connection stability
- Restart the application: Stop with `Ctrl+C`, then run `python run.py`
- Ensure port 8000 isn't blocked by firewall
- Close other bandwidth-intensive applications
- Try using a wired internet connection instead of Wi-Fi

#### WebSocket Connection Failures
**Issue**: Real-time features not working properly
**Solutions**:
- Check browser console (F12) for error messages
- Verify WebSocket support in your browser
- Disable browser extensions that might block WebSockets
- Try incognito/private browsing mode
- Restart both browser and application

### Getting Additional Help
If you continue experiencing issues:
1. Check the browser developer console (F12) for detailed error messages
2. Review the terminal output where you ran `python run.py`
3. Ensure all dependencies are properly installed: `pip install -r requirements.txt`
4. Try running in a fresh Python virtual environment

## 🎯 Advanced Usage

### Customizing AI Personality
You can modify Meraki's personality by editing the `AI_SYSTEM_PROMPT` variable in `app.py`. This allows you to:
- Change the AI's speaking style
- Adjust response length and tone
- Add specific knowledge domains
- Modify greeting patterns

### Development and Extension
The modular architecture makes it easy to add new features:
- **New API Integrations**: Follow the existing pattern in `app.py`
- **UI Customization**: Modify `templates/index.html` and `static/style.css`
- **Additional WebSocket Endpoints**: Extend the WebSocket handler
- **Custom Voice Models**: Integrate different TTS providers

## 📄 License and Credits

This project is designed to demonstrate modern AI voice interaction capabilities using cutting-edge APIs and technologies. It showcases the integration of multiple AI services to create a seamless conversational experience.

**Technologies Used**:
- FastAPI for robust backend API development
- WebSocket for real-time bidirectional communication
- AssemblyAI for accurate speech recognition
- Google Gemini for intelligent AI responses
- Murf AI for natural voice synthesis
- Modern web technologies for responsive UI

---



