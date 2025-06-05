import os
import streamlit as st
import requests
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import OllamaLLM
import json

# Import version information
try:
    from version import __version__, get_version_info
except ImportError:
    __version__ = "2.0.0"
    get_version_info = lambda: {"version": __version__}

# Load the environment variables from your .env file
load_dotenv()

# ==============================================================================
# ===== VLM-STUDIO LITE ========================================================
# ==============================================================================

# --- Page Config ---
st.set_page_config(
    page_title=f"VLM-Studio Lite v{__version__}", 
    layout="wide",
    initial_sidebar_state="expanded"
)
# Removed the logo display for now
# st.image("vc2.png", width=200)
st.title(f"🚀 VLM-Studio Lite v{__version__}")
st.caption("Multi-Agent AI Development Platform with Enhanced Monitoring")
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
        st.success("Crew launched! Agents are now working on your mission...")
        st.header("2. The Cosmic Dance")
        log_container = st.container()
        
        # Update agent status to Active
        import datetime
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Update Architect status
        architect_idx = next(i for i, agent in enumerate(st.session_state.agents) if agent["name"] == "Architect")
        st.session_state.agents[architect_idx]["status"] = "Active"
        st.session_state.agents[architect_idx]["current_task"] = "Creating software architecture plan"
        st.session_state.agents[architect_idx]["last_active"] = current_time
        
        log_container.write("🧘‍♂️ The crew is assembling...")
        log_container.write("🤖 Architect agent is now active - creating the plan...")

        # Prepare messages for backend
        messages = [
            {"role": "system", "content": "You are a legendary software architect. Create a detailed, step-by-step plan with filenames and full code for each file."},
            {"role": "user", "content": mission}
        ]
        
        with st.spinner("Architect is thinking..."):
            backend_result = call_backend_chat_api(provider, model_name, messages)
            
        if backend_result and "response" in backend_result:
            plan_result = backend_result["response"]["content"]
            
            # Update Architect completion
            st.session_state.agents[architect_idx]["status"] = "Ready"
            st.session_state.agents[architect_idx]["current_task"] = "Plan completed"
            st.session_state.agents[architect_idx]["tasks_completed"] += 1
            st.session_state.agents[architect_idx]["history"].append(f"✅ Created plan for: {mission[:50]}...")
            
            log_container.write("✅ The Architect has returned with a plan:")
            st.markdown(plan_result)

            # --- Activate Coder Agent ---
            coder_idx = next(i for i, agent in enumerate(st.session_state.agents) if agent["name"] == "Coder")
            st.session_state.agents[coder_idx]["status"] = "Active"
            st.session_state.agents[coder_idx]["current_task"] = "Writing code files"
            st.session_state.agents[coder_idx]["last_active"] = current_time
            
            log_container.write("\n💻 The Coder is now manifesting the files...")
            
            with st.spinner("Coder is writing files..."):
                project_path = "./generated_project"
                if not os.path.exists(project_path):
                    os.makedirs(project_path)

                # A simple parser for the plan format
                files_created = 0
                files = plan_result.split('File: ')
                for f in files[1:]:
                    try:
                        file_path_str, code_block = f.split('\n', 1)
                        code = code_block.strip().replace('```python', '').replace('```', '').strip()
                        full_path = os.path.join(project_path, file_path_str.strip())
                        
                        # Create directory if it doesn't exist
                        os.makedirs(os.path.dirname(full_path), exist_ok=True)
                        
                        with open(full_path, 'w') as code_file:
                            code_file.write(code)
                        log_container.write(f"   - ✅ Wrote code to {full_path}")
                        files_created += 1
                    except Exception as e:
                        st.error(f"Error writing file: {e}")
                        # Update agent with error status
                        st.session_state.agents[coder_idx]["history"].append(f"❌ Error writing file: {str(e)}")

            # Update Coder completion
            st.session_state.agents[coder_idx]["status"] = "Ready"
            st.session_state.agents[coder_idx]["current_task"] = f"Completed - {files_created} files created"
            st.session_state.agents[coder_idx]["tasks_completed"] += 1
            st.session_state.agents[coder_idx]["history"].append(f"✅ Created {files_created} files for project")

            st.success(f"🚀 Mission Accomplished using {provider} ({model_name})! The code has been manifested in the 'generated_project' directory.")
            st.info(f"📊 Total files created: {files_created}")
            st.balloons()
        else:
            # Update agent status on failure
            st.session_state.agents[architect_idx]["status"] = "Error"
            st.session_state.agents[architect_idx]["current_task"] = "Failed to create plan"
            st.session_state.agents[architect_idx]["history"].append("❌ Failed to generate plan - backend error")
            
            st.error(f"The cosmic dance encountered turbulence: {backend_result.get('error', 'Unknown error') if backend_result else 'No response from backend.'}")

# --- Agent Information Display ---
st.header("🤖 Agent Monitoring & Control Center")

# Initialize session state for agent data
if 'agents' not in st.session_state:
    st.session_state.agents = [
        {
            "name": "Architect",
            "role": "Principal Software Architect",
            "status": "Ready",
            "last_active": "2024-01-15 10:30:00",
            "tasks_completed": 5,
            "current_task": "None",
            "history": [
                "✅ Created Flask application architecture",
                "✅ Reviewed code structure for mission requirements",
                "✅ Generated detailed implementation plan"
            ],
            "configuration": {
                "temperature": 0.7,
                "max_tokens": 2000,
                "verbose": True
            }
        },
        {
            "name": "Coder",
            "role": "Senior Software Engineer",
            "status": "Ready",
            "last_active": "2024-01-15 10:25:00",
            "tasks_completed": 3,
            "current_task": "None",
            "history": [
                "✅ Implemented Flask hello world endpoint",
                "✅ Created proper file structure",
                "✅ Fixed syntax errors in generated code"
            ],
            "configuration": {
                "temperature": 0.3,
                "max_tokens": 3000,
                "verbose": True
            }
        }
    ]

# Create tabs for different monitoring views
tab1, tab2, tab3 = st.tabs(["📊 Agent Dashboard", "⚙️ Agent Configuration", "📈 Performance Metrics"])

with tab1:
    # Display agent status cards
    col1, col2 = st.columns(2)
    
    for i, agent in enumerate(st.session_state.agents):
        with col1 if i % 2 == 0 else col2:
            with st.container():
                # Status indicator
                status_color = {
                    "Active": "🟢",
                    "Ready": "🟡",
                    "Idle": "⚪",
                    "Error": "🔴"
                }.get(agent["status"], "⚪")
                
                st.markdown(f"### {status_color} {agent['name']}")
                st.markdown(f"**Role:** {agent['role']}")
                st.markdown(f"**Status:** {agent['status']}")
                st.markdown(f"**Current Task:** {agent['current_task']}")
                st.markdown(f"**Last Active:** {agent['last_active']}")
                st.markdown(f"**Tasks Completed:** {agent['tasks_completed']}")
                
                # Recent activity
                with st.expander("📋 Recent Activity"):
                    for entry in agent["history"][-3:]:  # Show last 3 entries
                        st.markdown(f"• {entry}")
                
                # Quick actions
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button(f"Reset {agent['name']}", key=f"reset_{agent['name']}"):
                        st.session_state.agents[i]["status"] = "Ready"
                        st.session_state.agents[i]["current_task"] = "None"
                        st.rerun()
                with col_b:
                    if st.button(f"View Details", key=f"details_{agent['name']}"):
                        st.info(f"Detailed view for {agent['name']} - Configuration: {agent['configuration']}")

with tab2:
    st.subheader("🔧 Dynamic Agent Configuration")
    
    # Agent selector
    selected_agent_name = st.selectbox(
        "Select Agent to Configure:",
        [agent["name"] for agent in st.session_state.agents]
    )
    
    # Find selected agent
    selected_agent_idx = next(
        i for i, agent in enumerate(st.session_state.agents) 
        if agent["name"] == selected_agent_name
    )
    selected_agent = st.session_state.agents[selected_agent_idx]
    
    # Configuration options
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Basic Settings**")
        new_role = st.text_input(
            "Role:", 
            value=selected_agent["role"],
            key=f"role_{selected_agent_name}"
        )
        
        new_temperature = st.slider(
            "Temperature (Creativity):",
            min_value=0.0,
            max_value=2.0,
            value=selected_agent["configuration"]["temperature"],
            step=0.1,
            key=f"temp_{selected_agent_name}"
        )
        
        new_max_tokens = st.number_input(
            "Max Tokens:",
            min_value=100,
            max_value=8000,
            value=selected_agent["configuration"]["max_tokens"],
            step=100,
            key=f"tokens_{selected_agent_name}"
        )
    
    with col2:
        st.markdown("**Advanced Settings**")
        new_verbose = st.checkbox(
            "Verbose Output",
            value=selected_agent["configuration"]["verbose"],
            key=f"verbose_{selected_agent_name}"
        )
        
        # Custom instructions
        custom_instructions = st.text_area(
            "Custom Instructions:",
            placeholder="Enter any specific instructions for this agent...",
            key=f"instructions_{selected_agent_name}"
        )
    
    # Update configuration
    if st.button("💾 Update Configuration", key=f"update_{selected_agent_name}"):
        st.session_state.agents[selected_agent_idx]["role"] = new_role
        st.session_state.agents[selected_agent_idx]["configuration"].update({
            "temperature": new_temperature,
            "max_tokens": new_max_tokens,
            "verbose": new_verbose
        })
        
        # Add to history
        st.session_state.agents[selected_agent_idx]["history"].append(
            f"🔧 Configuration updated: temp={new_temperature}, tokens={new_max_tokens}"
        )
        
        st.success(f"✅ Configuration updated for {selected_agent_name}")
        st.rerun()

with tab3:
    st.subheader("📈 Agent Performance Metrics")
    
    # Create metrics visualization
    col1, col2, col3 = st.columns(3)
    
    total_tasks = sum(agent["tasks_completed"] for agent in st.session_state.agents)
    active_agents = sum(1 for agent in st.session_state.agents if agent["status"] == "Active")
    
    with col1:
        st.metric("Total Tasks Completed", total_tasks)
    with col2:
        st.metric("Active Agents", active_agents, delta=f"{len(st.session_state.agents) - active_agents} idle")
    with col3:
        avg_tasks = total_tasks / len(st.session_state.agents) if st.session_state.agents else 0
        st.metric("Avg Tasks per Agent", f"{avg_tasks:.1f}")
    
    # Agent performance comparison
    st.markdown("**📊 Agent Task Completion**")
    agent_names = [agent["name"] for agent in st.session_state.agents]
    task_counts = [agent["tasks_completed"] for agent in st.session_state.agents]
    
    # Simple bar chart using Streamlit's built-in chart
    import pandas as pd
    chart_data = pd.DataFrame({
        "Agent": agent_names,
        "Tasks Completed": task_counts
    })
    st.bar_chart(chart_data.set_index("Agent"))
    
    # Real-time monitoring toggle
    st.markdown("**🔄 Real-time Monitoring**")
    auto_refresh = st.checkbox("Enable Auto-refresh (5 seconds)")
    
    if auto_refresh:
        import time
        time.sleep(5)
        st.rerun()

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
