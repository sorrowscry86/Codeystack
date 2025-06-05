import os
import streamlit as st
import requests
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import OllamaLLM
import json

# Load the environment variables from your .env file
load_dotenv()

# ==============================================================================
# ===== VLM-STUDIO LITE ========================================================
# ==============================================================================

# --- Page Config ---
st.set_page_config(page_title="VLM-Studio Lite", layout="wide")
# Removed the logo display for now
# st.image("vc2.png", width=200)
st.title("🚀 VLM-Studio Lite")
st.write("Inspired by the Newbs guide to AI Agents, this is a simpler, more chill way to build.")

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:5000")

# --- LLM Provider Configuration ---
def configure_llm_provider(provider, model_name, api_key=None, base_url=None):
    """Configure and return the appropriate LLM based on provider selection."""
    
    if provider == "OpenAI":
        if not api_key:
            st.error("OpenAI API key is required.")
            return None
        os.environ["OPENAI_API_KEY"] = api_key
        return ChatOpenAI(model=model_name, temperature=0.7)
    
    elif provider == "Gemini":
        if not api_key:
            st.error("Gemini API key is required.")
            return None
        os.environ["GOOGLE_API_KEY"] = api_key
        return ChatGoogleGenerativeAI(model=model_name, temperature=0.7)
    
    elif provider == "OpenRouter":
        if not api_key:
            st.error("OpenRouter API key is required.")
            return None
        # OpenRouter uses OpenAI-compatible API
        return ChatOpenAI(
            model=model_name,
            openai_api_key=api_key,
            openai_api_base="https://openrouter.ai/api/v1",
            temperature=0.7
        )
    
    elif provider == "Ollama":
        if not base_url:
            st.error("Ollama base URL is required.")
            return None
        try:
            # Test Ollama connection
            response = requests.get(f"{base_url}/api/tags", timeout=3)
            response.raise_for_status()
        except requests.exceptions.RequestException:
            st.error("Could not connect to Ollama server. Is it running?")
            return None
        return OllamaLLM(model=model_name, base_url=base_url, temperature=0.7)
    
    elif provider == "LM Studio":
        if not base_url:
            st.error("LM Studio base URL is required.")
            return None
        try:
            # Test LM Studio connection
            response = requests.get(f"{base_url}/v1/models", timeout=3)
            response.raise_for_status()
        except requests.exceptions.RequestException:
            st.error("Could not connect to LM Studio server. Is it running?")
            return None
        return OllamaLLM(model=model_name, base_url=base_url, temperature=0.7)
    
    elif provider == "KoboldCpp":
        if not base_url:
            st.error("KoboldCpp base URL is required.")
            return None
        try:
            # Test KoboldCpp connection
            response = requests.get(f"{base_url}/api/status", timeout=3)
            response.raise_for_status()
        except requests.exceptions.RequestException:
            st.error("Could not connect to KoboldCpp server. Is it running?")
            return None
        return OllamaLLM(model=model_name, base_url=base_url, temperature=0.7)
    
    return None

# --- Sidebar for LLM Configuration ---
with st.sidebar:
    st.header("🤖 LLM Configuration")
    
    # Provider selection
    provider = st.selectbox(
        "Choose LLM Provider:",
        ["Gemini", "OpenAI", "OpenRouter", "Ollama", "LM Studio", "KoboldCpp"],
        index=0
    )
    
    # Model and API key configuration based on provider
    if provider == "OpenAI":
        api_key = st.text_input(
            "OpenAI API Key:", 
            value=os.getenv("OPENAI_API_KEY", ""), 
            type="password"
        )
        model_name = st.text_input(
            "Model Name:", 
            value=os.getenv("DEFAULT_OPENAI_MODEL", "gpt-4o-mini")
        )
        llm = configure_llm_provider(provider, model_name, api_key)
        
    elif provider == "Gemini":
        api_key = st.text_input(
            "Gemini API Key:", 
            value=os.getenv("GEMINI_API_KEY", ""), 
            type="password"
        )
        model_name = st.text_input(
            "Model Name:", 
            value=os.getenv("DEFAULT_GEMINI_MODEL", "gemini-1.5-flash")
        )
        llm = configure_llm_provider(provider, model_name, api_key)
        
    elif provider == "OpenRouter":
        api_key = st.text_input(
            "OpenRouter API Key:", 
            value=os.getenv("OPENROUTER_API_KEY", ""), 
            type="password"
        )
        model_name = st.text_input(
            "Model Name:", 
            value=os.getenv("DEFAULT_OPENROUTER_MODEL", "anthropic/claude-3.5-sonnet")
        )
        st.info("💡 Popular models: anthropic/claude-3.5-sonnet, openai/gpt-4o, meta-llama/llama-3.1-70b-instruct")
        llm = configure_llm_provider(provider, model_name, api_key)
        
    elif provider == "Ollama":
        base_url = st.text_input(
            "Ollama Base URL:", 
            value=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        )
        # Fetch Ollama models dynamically via HTTP
        models = []
        try:
            response = requests.get(f"{base_url}/api/tags", timeout=3)
            response.raise_for_status()
            tags = response.json().get("models", [])
            models = [tag["name"] for tag in tags]
        except Exception as e:
            st.error(f"Could not fetch Ollama models: {e}")
            models = ["llama2", "mistral", "codellama"]
        model_name = st.selectbox("Model Name:", options=models)
        st.info("💡 Make sure Ollama is running and the model is pulled!")
        llm = configure_llm_provider(provider, model_name, base_url=base_url)
    
    elif provider == "LM Studio":
        base_url = st.text_input(
            "LM Studio Base URL:", 
            value=os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234")
        )
        # Fetch LM Studio models dynamically via HTTP
        models = []
        try:
            response = requests.get(f"{base_url}/v1/models", timeout=3)
            response.raise_for_status()
            tags = response.json().get("models", [])
            models = [tag["name"] for tag in tags]
        except Exception as e:
            st.error(f"Could not fetch LM Studio models: {e}")
            models = ["default-model"]
        model_name = st.selectbox("Model Name:", options=models)
        st.info("💡 Make sure LM Studio is running and the model is pulled!")
        llm = configure_llm_provider(provider, model_name, base_url=base_url)

    elif provider == "KoboldCpp":
        base_url = st.text_input(
            "KoboldCpp Base URL:", 
            value=os.getenv("KOBOLDCPP_BASE_URL", "http://localhost:8080")
        )
        # KoboldCpp models are assumed to be static for now
        model_name = st.selectbox(
            "Model Name:", 
            options=["kobold-default", "kobold-advanced"]
        )
        llm = configure_llm_provider(provider, model_name, base_url=base_url)

    # Display current configuration
    if llm:
        st.success(f"LLM configured: {provider} - {model_name}")
    else:
        st.warning("LLM is not configured. Please check your settings.")

# --- Agent Definitions ---
# CrewAI makes it super easy to define agents with roles and goals.

def create_agents(llm=None):
    """Create agents with the specified LLM."""
    
    # The Architect Agent
    architect = Agent(
        role='Principal Software Architect',
        goal='Create a detailed, step-by-step plan for a given software mission. The plan must consist of filenames and the full code for each file.',
        backstory="You are a legendary software architect, known for your clarity and ability to turn any idea into a functional, elegant plan. You think step-by-step and produce code that is clean and direct.",
        verbose=True,
        allow_delegation=False,
        llm=llm  # Use the configured LLM
    )

    # The Coder Agent
    coder = Agent(
        role='Senior Software Engineer',
        goal='Take a plan from the architect and write the code to disk. You must write the files exactly as specified in the plan.',
        backstory="You are a master coder, a true craftsman of the digital age. You take architectural plans and manifest them into reality, writing clean, efficient code and saving it to the specified files.",
        verbose=True,
        allow_delegation=False,
        llm=llm  # Use the configured LLM
    )
    
    return architect, coder

# --- UI Elements ---
st.header("1. Define the Mission")
mission = st.text_area("What masterpiece shall the agents create today?", height=100,
                       value="Create a simple Python Flask web app with a single endpoint that returns a JSON 'hello world' message.")

def call_backend_chat_api(provider, model, messages, temperature=0.7, max_tokens=None):
    """Call the Flask backend /chat endpoint with the given parameters."""
    url = f"{BACKEND_URL}/chat"
    # Normalize provider name for backend
    provider_key = provider.lower().replace(" ", "")
    payload = {
        "provider": provider_key,
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        try:
            error_detail = response.json().get('error', str(e))
        except Exception:
            error_detail = str(e)
        st.error(f"Backend error: {error_detail}")
        return None
    except Exception as e:
        st.error(f"Backend error: {e}")
        return None

if st.button("✨ Launch the Crew"):
    if not llm:
        st.error("LLM is not configured. Please check your settings.")
    else:
        st.success("Crew launched! (This is a placeholder for actual agent execution.)")
        st.header("2. The Cosmic Dance")
        log_container = st.container()
        log_container.write("🧘‍♂️ The crew is assembling...")

        # Prepare messages for backend
        messages = [
            {"role": "system", "content": "You are a legendary software architect."},
            {"role": "user", "content": mission}
        ]
        backend_result = call_backend_chat_api(provider, model_name, messages)
        if backend_result and "response" in backend_result:
            plan_result = backend_result["response"]["content"]
            log_container.write("✅ The Architect has returned with a plan:")
            st.markdown(plan_result)

            # --- Coder Writes the Files ---
            log_container.write("\n💻 The Coder is now manifesting the files...")
            project_path = "./generated_project"
            if not os.path.exists(project_path):
                os.makedirs(project_path)

            # A simple parser for the plan format
            files = plan_result.split('File: ')
            for f in files[1:]:
                try:
                    file_path_str, code_block = f.split('\n', 1)
                    code = code_block.strip().replace('```python', '').replace('```', '').strip()
                    full_path = os.path.join(project_path, file_path_str.strip())
                    with open(full_path, 'w') as code_file:
                        code_file.write(code)
                    log_container.write(f"   - ✅ Wrote code to {full_path}")
                except Exception as e:
                    st.error(f"Bummer, the coder wiped out while writing a file: {e}")

            st.success(f"🚀 Mission Accomplished using {provider} ({model_name})! The code has been manifested in the 'generated_project' directory.")
            st.balloons()
        else:
            st.error(f"The cosmic dance encountered turbulence: {backend_result.get('error', 'Unknown error') if backend_result else 'No response from backend.'}")

# --- Footer Info ---
st.markdown("---")
st.markdown("### 🔧 Supported LLM Providers")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("**OpenAI**")
    st.markdown("- GPT-4o, GPT-4o-mini")
    st.markdown("- GPT-3.5-turbo")

with col2:
    st.markdown("**Google Gemini**")
    st.markdown("- Gemini 1.5 Flash")
    st.markdown("- Gemini 1.5 Pro")

with col3:
    st.markdown("**OpenRouter**")
    st.markdown("- Claude 3.5 Sonnet")
    st.markdown("- Llama 3.1 70B")
    st.markdown("- Many more models!")

with col4:
    st.markdown("**Ollama (Local)**")
    st.markdown("- Llama 3.1")
    st.markdown("- Code Llama")
    st.markdown("- Custom models")
