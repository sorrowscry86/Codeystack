# 📚 API Documentation - VLM Studio Lite

This document provides comprehensive information about the VLM Studio Lite API endpoints, request/response formats, and integration examples.

## 🔗 Base URL

```
http://localhost:5000
```

## 📋 Table of Contents

1. [Authentication](#authentication)
2. [Core Endpoints](#core-endpoints)
3. [Provider Management](#provider-management)
4. [Chat Completions](#chat-completions)
5. [Model Management](#model-management)
6. [Error Handling](#error-handling)
7. [Examples](#examples)
8. [Rate Limiting](#rate-limiting)

---

## 🔐 Authentication

Currently, the API uses API keys configured per provider. No global authentication is required for the local deployment.

### Supported Authentication Methods:
- **API Keys**: Provider-specific keys (OpenAI, Google, OpenRouter, etc.)
- **Local Servers**: No authentication required (Ollama, LM Studio, KoboldCpp)

---

## 🎯 Core Endpoints

### **Health Check**
Get system status and available providers.

```http
GET /
```

**Response:**
```json
{
  "message": "Studio Lite Multi-LLM Provider API",
  "status": "running",
  "available_providers": [
    "openai",
    "anthropic", 
    "google",
    "ollama",
    "openrouter",
    "lmstudio",
    "koboldcpp"
  ],
  "timestamp": "2025-06-05T20:56:01Z"
}
```

---

## ⚙️ Provider Management

### **List All Providers**
Get detailed information about all configured providers.

```http
GET /providers
```

**Response:**
```json
{
  "providers": {
    "openai": {
      "name": "OpenAI",
      "status": "configured",
      "models": ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"],
      "requires_api_key": true
    },
    "ollama": {
      "name": "Ollama",
      "status": "available",
      "base_url": "http://localhost:11434",
      "models": ["llama3.1:latest", "mistral:latest"],
      "requires_api_key": false
    }
  }
}
```

### **Get Provider Configuration**
Retrieve specific provider settings.

```http
GET /config/{provider_name}
```

**Parameters:**
- `provider_name` (string): Provider identifier (openai, ollama, etc.)

**Response:**
```json
{
  "provider": "openai",
  "configuration": {
    "api_key_configured": true,
    "default_model": "gpt-4o-mini",
    "max_tokens": 4000,
    "temperature": 0.7
  }
}
```

### **Update Provider Configuration**
Modify provider settings.

```http
POST /config/{provider_name}
```

**Request Body:**
```json
{
  "api_key": "your-api-key",
  "default_model": "gpt-4o",
  "base_url": "https://api.openai.com/v1",
  "max_tokens": 2000,
  "temperature": 0.8
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Provider configuration updated",
  "provider": "openai"
}
```

---

## 💬 Chat Completions

### **Generate Chat Completion**
Send messages to any configured LLM provider.

```http
POST /chat
```

**Request Body:**
```json
{
  "provider": "openai",
  "model": "gpt-4o-mini",
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful assistant."
    },
    {
      "role": "user", 
      "content": "Hello, how are you?"
    }
  ],
  "temperature": 0.7,
  "max_tokens": 1000,
  "stream": false
}
```

**Parameters:**
- `provider` (string, required): LLM provider name
- `model` (string, required): Specific model to use
- `messages` (array, required): Conversation messages
- `temperature` (float, optional): Creativity control (0.0-2.0)
- `max_tokens` (integer, optional): Maximum response length
- `stream` (boolean, optional): Enable streaming responses

**Response:**
```json
{
  "response": {
    "content": "Hello! I'm doing well, thank you for asking. How can I help you today?",
    "role": "assistant"
  },
  "usage": {
    "prompt_tokens": 15,
    "completion_tokens": 18,
    "total_tokens": 33
  },
  "provider": "openai",
  "model": "gpt-4o-mini",
  "timestamp": "2025-06-05T20:56:01Z"
}
```

### **Provider-Specific Examples**

#### **OpenAI Request**
```json
{
  "provider": "openai",
  "model": "gpt-4o",
  "messages": [{"role": "user", "content": "Explain quantum computing"}],
  "temperature": 0.3
}
```

#### **Ollama Request**
```json
{
  "provider": "ollama", 
  "model": "llama3.1:latest",
  "messages": [{"role": "user", "content": "Write a Python function"}],
  "temperature": 0.7
}
```

#### **Google Gemini Request**
```json
{
  "provider": "google",
  "model": "gemini-1.5-flash",
  "messages": [{"role": "user", "content": "Summarize this article"}],
  "max_tokens": 500
}
```

---

## 🔧 Model Management

### **List Available Models**
Get models from all providers.

```http
GET /api/models
```

**Response:**
```json
{
  "models": {
    "openai": [
      {
        "id": "gpt-4o",
        "name": "GPT-4o",
        "context_length": 128000,
        "description": "Most capable model"
      },
      {
        "id": "gpt-4o-mini", 
        "name": "GPT-4o Mini",
        "context_length": 128000,
        "description": "Fast and efficient"
      }
    ],
    "ollama": [
      {
        "id": "llama3.1:latest",
        "name": "Llama 3.1 Latest",
        "size": "4.7GB",
        "context_length": 8192
      }
    ]
  }
}
```

### **Get Provider Models**
List models for a specific provider.

```http
GET /api/models/{provider_name}
```

**Response:**
```json
{
  "provider": "ollama",
  "models": [
    {
      "name": "llama3.1:latest",
      "size": "4.7GB",
      "modified": "2025-06-05T10:30:00Z"
    }
  ]
}
```

---

## ❌ Error Handling

### **Error Response Format**
All errors follow a consistent format:

```json
{
  "error": {
    "type": "validation_error",
    "message": "Invalid provider specified",
    "code": "INVALID_PROVIDER",
    "details": {
      "provider": "invalid_provider",
      "available_providers": ["openai", "ollama", "google"]
    }
  },
  "timestamp": "2025-06-05T20:56:01Z"
}
```

### **HTTP Status Codes**

| Code | Description | Example |
|------|-------------|---------|
| `200` | Success | Request completed successfully |
| `400` | Bad Request | Invalid parameters or request body |
| `401` | Unauthorized | Missing or invalid API key |
| `404` | Not Found | Provider or endpoint not found |
| `429` | Rate Limited | Too many requests |
| `500` | Server Error | Internal server error |
| `503` | Service Unavailable | Provider service is down |

### **Common Error Types**

#### **Provider Not Available**
```json
{
  "error": {
    "type": "provider_error",
    "message": "Provider 'ollama' is not available",
    "code": "PROVIDER_UNAVAILABLE"
  }
}
```

#### **Model Not Found**
```json
{
  "error": {
    "type": "model_error", 
    "message": "Model 'gpt-5' not found for provider 'openai'",
    "code": "MODEL_NOT_FOUND"
  }
}
```

#### **API Key Missing**
```json
{
  "error": {
    "type": "authentication_error",
    "message": "API key required for provider 'openai'",
    "code": "API_KEY_REQUIRED"
  }
}
```

---

## 📝 Examples

### **Python Client Example**

```python
import requests
import json

class VLMStudioClient:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
    
    def chat(self, provider, model, messages, **kwargs):
        """Send a chat completion request."""
        payload = {
            "provider": provider,
            "model": model, 
            "messages": messages,
            **kwargs
        }
        
        response = requests.post(
            f"{self.base_url}/chat",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API Error: {response.text}")
    
    def get_providers(self):
        """Get available providers."""
        response = requests.get(f"{self.base_url}/providers")
        return response.json()
    
    def get_models(self, provider=None):
        """Get available models."""
        url = f"{self.base_url}/api/models"
        if provider:
            url += f"/{provider}"
        response = requests.get(url)
        return response.json()

# Usage
client = VLMStudioClient()

# Chat with OpenAI
result = client.chat(
    provider="openai",
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a coding assistant."},
        {"role": "user", "content": "Write a Python function to calculate fibonacci numbers."}
    ],
    temperature=0.3,
    max_tokens=1000
)

print(result["response"]["content"])
```

### **JavaScript Client Example**

```javascript
class VLMStudioClient {
    constructor(baseUrl = 'http://localhost:5000') {
        this.baseUrl = baseUrl;
    }
    
    async chat(provider, model, messages, options = {}) {
        const payload = {
            provider,
            model,
            messages,
            ...options
        };
        
        const response = await fetch(`${this.baseUrl}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        
        if (!response.ok) {
            throw new Error(`API Error: ${await response.text()}`);
        }
        
        return await response.json();
    }
    
    async getProviders() {
        const response = await fetch(`${this.baseUrl}/providers`);
        return await response.json();
    }
}

// Usage
const client = new VLMStudioClient();

// Chat with Ollama
const result = await client.chat(
    'ollama',
    'llama3.1:latest',
    [
        { role: 'user', content: 'Explain machine learning in simple terms' }
    ],
    { temperature: 0.7 }
);

console.log(result.response.content);
```

### **cURL Examples**

#### **Health Check**
```bash
curl -X GET http://localhost:5000/
```

#### **Chat Completion**
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "openai",
    "model": "gpt-4o-mini", 
    "messages": [
      {"role": "user", "content": "Hello!"}
    ],
    "temperature": 0.7
  }'
```

#### **Get Models**
```bash
curl -X GET http://localhost:5000/api/models/ollama
```

---

## 🚦 Rate Limiting

### **Current Limits**
- **Local providers** (Ollama, LM Studio, KoboldCpp): No rate limiting
- **API providers** (OpenAI, Google, OpenRouter): Limited by provider's rate limits
- **Concurrent requests**: Up to 10 simultaneous requests

### **Rate Limit Headers**
API responses include rate limiting information:

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1625097600
```

### **Handling Rate Limits**
When rate limited, implement exponential backoff:

```python
import time
import random

def make_request_with_backoff(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if "rate limit" in str(e).lower() and attempt < max_retries - 1:
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                time.sleep(wait_time)
                continue
            raise e
```

---

## 🔧 Advanced Configuration

### **Environment Variables**

```bash
# API Keys
OPENAI_API_KEY=sk-your-key
GEMINI_API_KEY=your-gemini-key
OPENROUTER_API_KEY=sk-or-your-key

# Local Server URLs
OLLAMA_BASE_URL=http://localhost:11434
LMSTUDIO_BASE_URL=http://localhost:1234
KOBOLDCPP_BASE_URL=http://localhost:5001

# Backend Configuration
BACKEND_URL=http://localhost:5000
FLASK_ENV=development
FLASK_DEBUG=true
```

### **Provider-Specific Settings**

#### **OpenAI Configuration**
```json
{
  "api_key": "sk-your-key",
  "organization": "org-your-org",
  "base_url": "https://api.openai.com/v1",
  "timeout": 30,
  "max_retries": 3
}
```

#### **Ollama Configuration**
```json
{
  "base_url": "http://localhost:11434",
  "timeout": 60,
  "keep_alive": true,
  "num_ctx": 2048
}
```

---

## 📞 Support

For API-related questions:
- **GitHub Issues**: [Report API bugs](https://github.com/sorrowscry86/Codeystack/issues)
- **Documentation**: [Main README](../README.md)
- **Examples**: [Example Scripts](../examples/)

---

*Last updated: June 5, 2025*
