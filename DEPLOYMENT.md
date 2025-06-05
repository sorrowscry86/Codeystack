# 🚀 Deployment Guide - VLM Studio Lite

This guide provides step-by-step instructions for deploying VLM Studio Lite in various environments, from local development to production cloud deployments.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development](#local-development)
3. [Docker Deployment](#docker-deployment)
4. [Cloud Deployment](#cloud-deployment)
5. [Production Considerations](#production-considerations)
6. [Monitoring & Logging](#monitoring--logging)
7. [Troubleshooting](#troubleshooting)

---

## ✅ Prerequisites

### **System Requirements**
- **OS**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **Python**: 3.11 or higher
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Storage**: 2GB free space (more for local models)
- **Network**: Internet access for API providers

### **Required Software**
```bash
# Check Python version
python --version  # Should be 3.11+

# Check pip
pip --version

# Check git
git --version

# Optional: Docker
docker --version
docker-compose --version
```

### **API Keys & Services**
Obtain API keys for desired providers:
- **OpenAI**: [platform.openai.com](https://platform.openai.com)
- **Google Gemini**: [ai.google.dev](https://ai.google.dev)
- **OpenRouter**: [openrouter.ai](https://openrouter.ai)
- **Anthropic**: [console.anthropic.com](https://console.anthropic.com)

---

## 🏠 Local Development

### **1. Repository Setup**

```bash
# Clone repository
git clone https://github.com/sorrowscry86/Codeystack.git
cd Codeystack

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### **2. Environment Configuration**

Create `.env` file in project root:

```bash
# Core Configuration
FLASK_ENV=development
FLASK_DEBUG=true
BACKEND_URL=http://localhost:5000

# API Keys (add your actual keys)
OPENAI_API_KEY=sk-your-openai-key-here
GEMINI_API_KEY=your-gemini-key-here
OPENROUTER_API_KEY=sk-or-your-openrouter-key
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key

# Local Server URLs
OLLAMA_BASE_URL=http://localhost:11434
LMSTUDIO_BASE_URL=http://localhost:1234
KOBOLDCPP_BASE_URL=http://localhost:5001

# Default Models
DEFAULT_OPENAI_MODEL=gpt-4o-mini
DEFAULT_GEMINI_MODEL=gemini-1.5-flash
DEFAULT_OPENROUTER_MODEL=anthropic/claude-3.5-sonnet
```

### **3. Start Services**

**Terminal 1 - Backend:**
```bash
python app.py
```

**Terminal 2 - Frontend:**
```bash
streamlit run studio_lite.py --server.port 8501
```

### **4. Verify Installation**

```bash
# Test backend health
curl http://localhost:5000/

# Open frontend
# Navigate to http://localhost:8501
```

---

## 🐳 Docker Deployment

### **1. Single Container Deployment**

```bash
# Build image
docker build -t vlm-studio-lite .

# Run container
docker run -d \
  --name vlm-studio \
  -p 5000:5000 \
  -p 8501:8501 \
  -e OPENAI_API_KEY=your-key \
  -e GEMINI_API_KEY=your-key \
  vlm-studio-lite
```

### **2. Docker Compose Deployment**

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  vlm-studio:
    build: .
    ports:
      - "5000:5000"
      - "8501:8501"
    environment:
      - FLASK_ENV=production
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
      - OLLAMA_BASE_URL=http://ollama:11434
    volumes:
      - ./generated_project:/app/generated_project
      - ./logs:/app/logs
    restart: unless-stopped
    depends_on:
      - ollama

  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    restart: unless-stopped

volumes:
  ollama_data:
```

**Deploy:**
```bash
# Create .env file with your API keys
echo "OPENAI_API_KEY=your-key" > .env
echo "GEMINI_API_KEY=your-key" >> .env

# Start services
docker-compose up -d

# View logs
docker-compose logs -f vlm-studio
```

### **3. Docker with Local Models**

**Extended docker-compose.yml:**
```yaml
version: '3.8'

services:
  vlm-studio:
    build: .
    ports:
      - "5000:5000"
      - "8501:8501"
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
      - LMSTUDIO_BASE_URL=http://lmstudio:1234
    volumes:
      - ./generated_project:/app/generated_project
    depends_on:
      - ollama
      - lmstudio

  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    command: >
      sh -c "ollama serve &
             sleep 10 &&
             ollama pull llama3.1:latest &&
             ollama pull mistral:latest &&
             wait"

  lmstudio:
    image: lmstudio/lmstudio-server:latest
    ports:
      - "1234:1234"
    volumes:
      - lmstudio_models:/app/models

volumes:
  ollama_data:
  lmstudio_models:
```

---

## ☁️ Cloud Deployment

### **1. AWS Deployment**

#### **EC2 Instance Setup**

```bash
# Launch EC2 instance (t3.medium or larger)
# Connect via SSH

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone and deploy
git clone https://github.com/sorrowscry86/Codeystack.git
cd Codeystack

# Configure environment
nano .env  # Add your API keys

# Deploy
docker-compose up -d
```

#### **AWS Load Balancer Configuration**

**Application Load Balancer (ALB) setup:**
```yaml
# alb-config.yml
listeners:
  - port: 80
    protocol: HTTP
    target_groups:
      - name: vlm-backend
        port: 5000
        health_check: /
      - name: vlm-frontend  
        port: 8501
        health_check: /
        
routing_rules:
  - path: /api/*
    target: vlm-backend
  - path: /*
    target: vlm-frontend
```

### **2. Google Cloud Platform (GCP)**

#### **Cloud Run Deployment**

**Dockerfile.cloud:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Use environment variable for port
ENV PORT=8080
EXPOSE 8080

CMD ["python", "app.py"]
```

**Deploy commands:**
```bash
# Build and push to Container Registry
docker build -f Dockerfile.cloud -t gcr.io/PROJECT_ID/vlm-studio .
docker push gcr.io/PROJECT_ID/vlm-studio

# Deploy to Cloud Run
gcloud run deploy vlm-studio \
  --image gcr.io/PROJECT_ID/vlm-studio \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=your-key
```

### **3. Azure Deployment**

#### **Azure Container Instances**

**azure-deploy.yml:**
```yaml
apiVersion: 2019-12-01
location: eastus
name: vlm-studio-group
properties:
  containers:
  - name: vlm-studio
    properties:
      image: your-registry/vlm-studio:latest
      ports:
      - port: 5000
      - port: 8501
      environmentVariables:
      - name: OPENAI_API_KEY
        secureValue: your-key
      resources:
        requests:
          cpu: 2
          memoryInGb: 4
  osType: Linux
  ipAddress:
    type: Public
    ports:
    - protocol: tcp
      port: 5000
    - protocol: tcp
      port: 8501
```

**Deploy:**
```bash
az container create --resource-group myResourceGroup --file azure-deploy.yml
```

### **4. Kubernetes Deployment**

**k8s-deployment.yml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vlm-studio
spec:
  replicas: 3
  selector:
    matchLabels:
      app: vlm-studio
  template:
    metadata:
      labels:
        app: vlm-studio
    spec:
      containers:
      - name: vlm-studio
        image: vlm-studio:latest
        ports:
        - containerPort: 5000
        - containerPort: 8501
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: openai
---
apiVersion: v1
kind: Service
metadata:
  name: vlm-studio-service
spec:
  selector:
    app: vlm-studio
  ports:
  - name: backend
    port: 5000
    targetPort: 5000
  - name: frontend
    port: 8501
    targetPort: 8501
  type: LoadBalancer
```

---

## 🔒 Production Considerations

### **1. Security**

#### **Environment Variables**
```bash
# Use secrets management
# AWS: Systems Manager Parameter Store
# GCP: Secret Manager
# Azure: Key Vault

# Example: AWS SSM
aws ssm put-parameter \
  --name "/vlm-studio/openai-key" \
  --value "your-key" \
  --type "SecureString"
```

#### **Network Security**
```yaml
# docker-compose.prod.yml
version: '3.8'

networks:
  internal:
    driver: bridge
    internal: true
  external:
    driver: bridge

services:
  vlm-studio:
    networks:
      - internal
      - external
    # Only expose necessary ports
    ports:
      - "80:5000"  # Backend via reverse proxy
    # No direct frontend exposure
```

#### **Reverse Proxy (Nginx)**
```nginx
# nginx.conf
upstream backend {
    server vlm-studio:5000;
}

upstream frontend {
    server vlm-studio:8501;
}

server {
    listen 80;
    server_name your-domain.com;

    # Backend API
    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Frontend
    location / {
        proxy_pass http://frontend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        
        # WebSocket support for Streamlit
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### **2. Performance Optimization**

#### **Resource Limits**
```yaml
# docker-compose.prod.yml
services:
  vlm-studio:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
        reservations:
          cpus: '1.0'
          memory: 2G
      restart_policy:
        condition: on-failure
        max_attempts: 3
```

#### **Caching Strategy**
```python
# Add to app.py
from flask_caching import Cache

cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': 'redis://redis:6379/0',
    'CACHE_DEFAULT_TIMEOUT': 300
})

@app.route('/api/models')
@cache.cached(timeout=600)  # Cache for 10 minutes
def get_models():
    # Model fetching logic
    pass
```

### **3. Database Integration**

#### **PostgreSQL for Agent History**
```yaml
# docker-compose.prod.yml
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: vlm_studio
      POSTGRES_USER: vlm_user
      POSTGRES_PASSWORD: secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - internal

  vlm-studio:
    environment:
      - DATABASE_URL=postgresql://vlm_user:password@postgres:5432/vlm_studio
    depends_on:
      - postgres

volumes:
  postgres_data:
```

---

## 📊 Monitoring & Logging

### **1. Application Logging**

#### **Structured Logging**
```python
# Add to app.py
import logging
import json
from datetime import datetime

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)

def log_structured(level, message, **kwargs):
    log_entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'level': level,
        'message': message,
        **kwargs
    }
    logging.log(getattr(logging, level.upper()), json.dumps(log_entry))

# Usage
log_structured('info', 'Chat request received', 
               provider='openai', model='gpt-4o', user_id='123')
```

### **2. Health Checks**

#### **Enhanced Health Endpoint**
```python
@app.route('/health')
def health_check():
    """Comprehensive health check"""
    checks = {}
    
    # Check each provider
    for provider_name in PROVIDERS:
        try:
            provider = get_provider(provider_name)
            checks[provider_name] = provider.health_check()
        except Exception as e:
            checks[provider_name] = {'status': 'error', 'error': str(e)}
    
    # Overall status
    all_healthy = all(check.get('status') == 'healthy' for check in checks.values())
    
    return jsonify({
        'status': 'healthy' if all_healthy else 'degraded',
        'providers': checks,
        'timestamp': datetime.utcnow().isoformat()
    }), 200 if all_healthy else 503
```

### **3. Metrics Collection**

#### **Prometheus Integration**
```python
# Add to requirements.txt
# prometheus-client==0.16.0

from prometheus_client import Counter, Histogram, generate_latest

# Metrics
REQUEST_COUNT = Counter('vlm_requests_total', 'Total requests', ['provider', 'model'])
REQUEST_DURATION = Histogram('vlm_request_duration_seconds', 'Request duration')

@app.route('/metrics')
def metrics():
    return generate_latest()

# Usage in chat endpoint
@REQUEST_DURATION.time()
def chat():
    REQUEST_COUNT.labels(provider=provider, model=model).inc()
    # ... chat logic
```

### **4. Error Tracking**

#### **Sentry Integration**
```python
# Add to requirements.txt
# sentry-sdk[flask]==1.32.0

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()],
    traces_sample_rate=0.1
)
```

---

## 🔧 Troubleshooting

### **Common Issues**

#### **1. Port Conflicts**
```bash
# Check what's using ports
netstat -tulpn | grep :5000
netstat -tulpn | grep :8501

# Kill processes
sudo lsof -ti:5000 | xargs kill -9
sudo lsof -ti:8501 | xargs kill -9
```

#### **2. Docker Issues**
```bash
# Container logs
docker logs vlm-studio

# Interactive debugging
docker exec -it vlm-studio /bin/bash

# Rebuild without cache
docker-compose build --no-cache
```

#### **3. Provider Connection Issues**
```bash
# Test provider endpoints
curl -v https://api.openai.com/v1/models -H "Authorization: Bearer YOUR_KEY"
curl -v http://localhost:11434/api/tags  # Ollama
curl -v http://localhost:1234/v1/models  # LM Studio
```

#### **4. Memory Issues**
```bash
# Monitor memory usage
docker stats

# Increase Docker memory limits
# Docker Desktop -> Settings -> Resources -> Memory
```

### **Deployment Checklist**

- [ ] **Environment variables configured**
- [ ] **API keys secured (not in code)**
- [ ] **Health checks responding**
- [ ] **Logs structured and accessible**
- [ ] **Reverse proxy configured (if applicable)**
- [ ] **SSL certificates installed (production)**
- [ ] **Monitoring alerts configured**
- [ ] **Backup strategy implemented**
- [ ] **Resource limits set**
- [ ] **Network security configured**

### **Performance Tuning**

```bash
# System optimizations
echo 'vm.max_map_count=262144' >> /etc/sysctl.conf
echo 'fs.file-max=65536' >> /etc/sysctl.conf

# Docker optimizations
echo '{"default-ulimits":{"nofile":{"Hard":65536,"Name":"nofile","Soft":65536}}}' > /etc/docker/daemon.json
systemctl restart docker
```

---

## 📞 Support

For deployment assistance:
- **GitHub Issues**: [Deployment Problems](https://github.com/sorrowscry86/Codeystack/issues)
- **Documentation**: [Main README](../README.md)
- **API Docs**: [API Documentation](../API_DOCUMENTATION.md)

---

*Last updated: June 5, 2025*
