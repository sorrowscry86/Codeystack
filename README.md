# 🚀 VLM Studio Lite - Multi-Agent AI Development Platform

VLM Studio Lite is a comprehensive AI agent development platform that combines the power of CrewAI with multiple Large Language Model (LLM) providers. It features a modern Streamlit frontend with real-time agent monitoring and a robust Flask backend supporting 7 different LLM providers.

## ✨ Key Features

### 🤖 **Advanced Agent Monitoring & Control**
- **Real-time Agent Dashboard** with live status tracking (Active, Ready, Idle, Error)
- **Dynamic Agent Configuration** - adjust temperature, tokens, and behavior on-the-fly
- **Performance Metrics** with task completion tracking and visual analytics
- **Agent History Logging** with detailed activity records
- **Session Persistence** for agent configurations and state

### 🌐 **Multi-LLM Provider Support**
- **OpenAI**: GPT-4o, GPT-4o-mini, GPT-3.5-turbo
- **Google Gemini**: Gemini 1.5 Flash, Gemini 1.5 Pro
- **Anthropic**: Claude 3.5 Sonnet (via OpenRouter)
- **OpenRouter**: Access to 50+ models including Meta Llama, Claude, and more
- **Ollama**: Local model support with dynamic model detection
- **LM Studio**: Local model hosting with automatic model discovery
- **KoboldCpp**: Local inference server support

### 🎯 **CrewAI Integration**
- **Architect Agent**: Creates detailed software plans and architectures
- **Coder Agent**: Implements code based on architectural plans
- **File Generation**: Automatically creates project files with proper structure
- **Mission Execution**: End-to-end software development automation

### 🔧 **Developer Experience**
- **Interactive Streamlit UI** with modern, responsive design
- **RESTful API** for backend integration
- **Docker Support** for easy deployment
- **Live Progress Tracking** during agent execution
- **Error Handling** with detailed feedback and recovery

## 🚀 Quick Start

### Prerequisites
- **Python 3.11+** (recommended)
- **Git** for cloning the repository
- **Docker** (optional, for containerized deployment)
- **API Keys** for your chosen LLM providers

### Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/sorrowscry86/Codeystack.git
   cd Codeystack
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables** (optional)
   ```bash
   # Create .env file
   OPENAI_API_KEY=your_openai_key
   GEMINI_API_KEY=your_gemini_key
   OPENROUTER_API_KEY=your_openrouter_key
   OLLAMA_BASE_URL=http://localhost:11434
   LMSTUDIO_BASE_URL=http://localhost:1234
   ```

4. **Start the Backend Server**
   ```bash
   python app.py
   ```
   Backend will be available at `http://localhost:5000`

5. **Launch the Frontend**
   ```bash
   streamlit run studio_lite.py
   ```
   Frontend will be available at `http://localhost:8501`

## 📊 **Agent Monitoring Dashboard**

The enhanced agent monitoring system provides comprehensive oversight of your AI agents:

### **Dashboard Features**
- **🟢 Real-time Status Indicators**: Track agent states (Active, Ready, Idle, Error)
- **📋 Task History**: View recent agent activities and completed tasks
- **⚙️ Dynamic Configuration**: Adjust agent settings without restart
- **📈 Performance Metrics**: Monitor task completion rates and efficiency
- **🔄 Auto-refresh**: Optional real-time updates every 5 seconds

### **Agent Configuration Options**
- **Temperature Control**: Adjust creativity vs. consistency (0.0 - 2.0)
- **Token Limits**: Configure maximum response length (100 - 8000 tokens)
- **Verbose Mode**: Enable/disable detailed logging
- **Custom Instructions**: Add specific guidance for individual agents

## 🛠️ **API Endpoints**

### **Core Endpoints**
- `GET /` - Health check with available providers
- `POST /chat` - Generate completions with any supported provider
- `GET /providers` - List all configured LLM providers
- `GET /config/<provider>` - Get provider-specific configuration
- `POST /config/<provider>` - Update provider settings

### **Chat API Usage**
```python
import requests

# Example chat request
response = requests.post('http://localhost:5000/chat', json={
    "provider": "openai",
    "model": "gpt-4o-mini",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ],
    "temperature": 0.7,
    "max_tokens": 1000
})

result = response.json()
```

## 🐳 **Docker Deployment**

### **Quick Deploy with Docker Compose**
```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d --build
```

### **Manual Docker Build**
```bash
# Build the image
docker build -t vlm-studio-lite .

# Run the container
docker run -p 5000:5000 -p 8501:8501 vlm-studio-lite
```

### **Environment Variables for Docker**
```yaml
# docker-compose.yml environment section
environment:
  - OPENAI_API_KEY=${OPENAI_API_KEY}
  - GEMINI_API_KEY=${GEMINI_API_KEY}
  - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
  - OLLAMA_BASE_URL=http://host.docker.internal:11434
```

## 📁 **Project Structure**

```
Codeystack/
├── 📄 app.py                 # Flask backend server
├── 🎨 studio_lite.py         # Streamlit frontend with agent monitoring
├── 📋 requirements.txt       # Python dependencies
├── 🐳 Dockerfile            # Container configuration
├── 🔧 docker-compose.yml    # Multi-service deployment
├── 📖 README.md             # This documentation
├── 🖼️ vc2.png               # Application logo
├── 📝 test_llm_providers.py  # Provider testing utilities
├── config/                   # Configuration management
│   └── llm_config.py        # LLM provider configurations
├── llm_providers/           # Provider implementations
│   ├── __init__.py          # Provider exports
│   ├── base.py              # Base provider interface
│   ├── factory.py           # Provider factory pattern
│   ├── openai_provider.py   # OpenAI integration
│   ├── google_provider.py   # Google Gemini integration
│   ├── anthropic_provider.py# Anthropic Claude integration
│   ├── openrouter_provider.py# OpenRouter gateway
│   ├── ollama_provider.py   # Ollama local models
│   ├── lmstudio_provider.py # LM Studio integration
│   └── koboldcpp_provider.py# KoboldCpp integration
└── generated_project/       # Agent-generated code output
```

## 🎯 **Usage Examples**

### **1. Basic Mission Execution**
```markdown
Mission: "Create a simple Python Flask web API with authentication"

1. Select your preferred LLM provider in the sidebar
2. Configure API keys or local server URLs
3. Enter your mission description
4. Click "✨ Launch the Crew"
5. Monitor agent progress in real-time
6. Review generated code in the generated_project/ folder
```

### **2. Advanced Agent Configuration**
```markdown
1. Navigate to "Agent Monitoring & Control Center"
2. Select "⚙️ Agent Configuration" tab
3. Choose an agent (Architect or Coder)
4. Adjust settings:
   - Temperature: 0.3 (focused) to 1.0 (creative)
   - Max Tokens: 1000-4000 depending on complexity
   - Verbose: Enable for detailed logging
5. Click "💾 Update Configuration"
```

### **3. Performance Monitoring**
```markdown
1. Check "📈 Performance Metrics" tab
2. View total tasks completed
3. Monitor active agent count
4. Review individual agent performance
5. Enable auto-refresh for real-time updates
```

## 🔧 **Configuration Guide**

### **Provider-Specific Setup**

#### **OpenAI Configuration**
```python
# Required: API Key
OPENAI_API_KEY = "sk-your-key-here"
# Models: gpt-4o, gpt-4o-mini, gpt-3.5-turbo
```

#### **Google Gemini Configuration**
```python
# Required: API Key from Google AI Studio
GEMINI_API_KEY = "your-gemini-key"
# Models: gemini-1.5-flash, gemini-1.5-pro
```

#### **Ollama Configuration**
```python
# Required: Running Ollama server
OLLAMA_BASE_URL = "http://localhost:11434"
# Models: Auto-detected from running instance
# Setup: ollama pull llama3.1:latest
```

#### **LM Studio Configuration**
```python
# Required: Running LM Studio server
LMSTUDIO_BASE_URL = "http://localhost:1234"
# Models: Auto-detected from loaded models
# Setup: Load model in LM Studio, start server
```

## 🚨 **Troubleshooting**

### **Common Issues & Solutions**

#### **"LLM is not configured"**
- Verify API keys are correctly entered
- Check network connectivity for local servers
- Ensure the selected provider service is running

#### **"Could not connect to [Provider] server"**
- For Ollama: Run `ollama serve` and ensure port 11434 is open
- For LM Studio: Start the local server in LM Studio application
- For KoboldCpp: Launch KoboldCpp with `--port 5001` parameter

#### **Agent Status Stuck on "Active"**
- Check backend logs at `http://localhost:5000`
- Verify the selected model is available
- Try reducing max_tokens or adjusting temperature

#### **Generated Files Not Appearing**
- Check the `generated_project/` directory
- Verify write permissions in the project folder
- Review agent history in the monitoring dashboard

## 🤝 **Contributing**

We welcome contributions! Here's how to get started:

1. **Fork the Repository**
2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make Your Changes**
   - Add new LLM providers
   - Enhance agent capabilities
   - Improve the UI/UX
   - Fix bugs or add tests
4. **Commit Your Changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
5. **Push to Your Branch**
   ```bash
   git push origin feature/amazing-feature
   ```
6. **Open a Pull Request**

### **Development Guidelines**
- Follow PEP 8 for Python code style
- Add docstrings for new functions and classes
- Update README.md for new features
- Test with multiple LLM providers
- Ensure Docker compatibility

## 📊 **Roadmap**

### **Upcoming Features**
- [ ] **WebSocket Integration** for real-time agent updates
- [ ] **Custom Agent Templates** for specialized workflows
- [ ] **Multi-Mission Queue** for concurrent task processing
- [ ] **Agent Collaboration Logs** with interaction history
- [ ] **Export/Import Configurations** for team sharing
- [ ] **Advanced Metrics Dashboard** with charts and analytics
- [ ] **Plugin System** for community extensions
- [ ] **Cloud Deployment Templates** for AWS/Azure/GCP

### **Requested Enhancements**
- [ ] **Voice Interface** for hands-free operation
- [ ] **Code Review Agent** for quality assurance
- [ ] **Documentation Agent** for auto-generated docs
- [ ] **Testing Agent** for automated test creation
- [ ] **Deployment Agent** for CI/CD integration

## 📄 **License**

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 VLM Studio Lite Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

## 🙏 **Acknowledgments**

- **CrewAI Team** for the amazing multi-agent framework
- **Streamlit** for the intuitive web app framework
- **Flask** for the lightweight backend framework
- **LangChain** for LLM integration utilities
- **Community Contributors** who make this project better

## 📞 **Support & Contact**

- **GitHub Issues**: [Report bugs or request features](https://github.com/sorrowscry86/Codeystack/issues)
- **Discussions**: [Community discussions and Q&A](https://github.com/sorrowscry86/Codeystack/discussions)
- **Developer**: [@sorrowscry86](https://github.com/sorrowscry86)
- **Project**: [Codeystack Repository](https://github.com/sorrowscry86/Codeystack)
- **Contact**: Wykeve Freeman (Sorrow Eternal) - SorrowsCry86@voidcat.org
- **Organization**: VoidCat RDC

---

<div align="center">

**⭐ Star this repository if it helped you!**

Made with ❤️ by the VLM Studio Lite community

</div>
