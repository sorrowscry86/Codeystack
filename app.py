"""
Flask Application with Multi-LLM Provider Integration
Test API for Studio Lite LLM functionality
"""

from flask import Flask, request, jsonify
from typing import Dict, Any
import traceback
import logging

from llm_providers.factory import LLMProviderFactory
from llm_providers.base import ChatMessage
from config.llm_config import LLMConfigManager

# Import version information
try:
    from version import __version__, get_version_info
except ImportError:
    __version__ = "2.0.0"
    get_version_info = lambda: {"version": __version__}

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
config_manager = LLMConfigManager()


@app.route('/')
def index():
    """Health check endpoint"""
    version_info = get_version_info()
    return jsonify({
        'status': 'healthy',
        'service': 'VLM Studio Lite Backend',
        'version': __version__,
        'build_info': version_info,
        'message': 'Multi-Agent AI Development Platform Backend is running'
    })


@app.route('/providers', methods=['GET'])
def get_providers():
    """Get available providers and their configurations"""
    providers_info = {}
    
    for provider_name in LLMProviderFactory.get_available_providers():
        config = config_manager.get_config(provider_name)
        providers_info[provider_name] = {
            'available_models': config.get('available_models', []),
            'default_model': config.get('default_model'),
            'configured': config_manager.validate_provider_config(provider_name)
        }
    
    return jsonify({
        'providers': providers_info,
        'total_providers': len(providers_info)
    })


@app.route('/chat', methods=['POST'])
def chat():
    """Chat completion endpoint"""
    try:
        data = request.get_json()
        print("[DEBUG] Incoming /chat request data:", data)
        if not data:
            print("[DEBUG] No data received in request body.")
            return jsonify({'error': 'Missing request data'}), 400
        
        # Extract parameters
        provider_name = data.get('provider', 'openai')
        model = data.get('model')
        messages_data = data.get('messages', [])
        temperature = data.get('temperature', 0.7)
        max_tokens = data.get('max_tokens')
        print(f"[DEBUG] provider: {provider_name}, model: {model}, messages: {messages_data}, temperature: {temperature}, max_tokens: {max_tokens}")
        
        if not messages_data:
            print("[DEBUG] Missing messages field or empty list.")
            return jsonify({'error': 'Missing messages'}), 400
        
        # Convert message data to ChatMessage objects
        messages = []
        for msg_data in messages_data:
            if not isinstance(msg_data, dict) or 'role' not in msg_data or 'content' not in msg_data:
                print(f"[DEBUG] Invalid message format: {msg_data}")
                return jsonify({'error': 'Invalid message format'}), 400
            messages.append(ChatMessage(
                role=msg_data['role'],
                content=msg_data['content']
            ))
        
        # Get provider configuration
        provider_config = config_manager.get_config(provider_name)
        print(f"[DEBUG] provider_config: {provider_config}")
        
        if not provider_config:
            print(f"[DEBUG] Provider config not found for: {provider_name}")
            return jsonify({'error': f'Provider config not found: {provider_name}'}), 400
        
        # Create provider instance
        provider = LLMProviderFactory.create_provider(provider_name, provider_config)
        print(f"[DEBUG] Created provider instance: {provider}")
        
        # Generate response
        response = provider.chat_completion(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens
        )
        print(f"[DEBUG] Provider response: {response}")
        
        return jsonify({
            'response': {
                'content': response.content,
                'model': response.model,
                'provider': response.provider,
                'metadata': response.metadata
            },
            'request_info': {
                'provider': provider_name,
                'model': model or provider_config.get('default_model'),
                'temperature': temperature,
                'max_tokens': max_tokens,
                'message_count': len(messages)
            }
        })
    
    except ValueError as e:
        print(f"[DEBUG] ValueError: {e}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print(f"[DEBUG] Exception: {e}")
        import traceback
        print(traceback.format_exc())
        return jsonify({
            'error': 'Internal server error',
            'details': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/test/<provider_name>', methods=['POST'])
def test_provider(provider_name):
    """Test a specific provider with a simple message"""
    try:
        # Get provider configuration
        provider_config = config_manager.get_config(provider_name)
        
        if not provider_config:
            return jsonify({'error': f'Provider "{provider_name}" not found'}), 400
        
        # Create provider instance
        provider = LLMProviderFactory.create_provider(provider_name, provider_config)
        
        # Test with a simple message
        test_messages = [ChatMessage(role='user', content='Hello! Please respond with just "Test successful"')]
        
        response = provider.chat_completion(
            messages=test_messages,
            temperature=0.1,
            max_tokens=50
        )
        
        return jsonify({
            'status': 'success',
            'provider': provider_name,
            'response': response.content,
            'model': response.model,
            'configured': config_manager.validate_provider_config(provider_name)
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'provider': provider_name,
            'error': str(e),
            'configured': config_manager.validate_provider_config(provider_name)
        }), 500


@app.route('/config/<provider_name>', methods=['GET', 'POST'])
def manage_config(provider_name):
    """Get or update provider configuration"""
    if request.method == 'GET':
        config = config_manager.get_config(provider_name)
        # Remove sensitive information
        safe_config = {k: v for k, v in config.items() if 'key' not in k.lower()}
        return jsonify({
            'provider': provider_name,
            'config': safe_config,
            'configured': config_manager.validate_provider_config(provider_name)
        })
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'Missing config data'}), 400
            
            config_manager.update_config(provider_name, data)
            
            return jsonify({'status': 'success', 'provider': provider_name, 'updated_config': data})
        
        except Exception as e:
            return jsonify({'status': 'error', 'provider': provider_name, 'error': str(e)}), 500


@app.route('/api/models', methods=['GET'])
def get_models():
    """Return a list of available models for all providers (static placeholder)."""
    # Example: aggregate all models from all providers
    providers = LLMProviderFactory.get_available_providers()
    models = {}
    for provider in providers:
        config = config_manager.get_config(provider)
        models[provider] = config.get('available_models', [])
    return jsonify({'models': models})


if __name__ == '__main__':
    print("Starting Studio Lite Multi-LLM Provider API...")
    print(f"Available providers: {LLMProviderFactory.get_available_providers()}")
    
    # Print configuration status
    for provider in LLMProviderFactory.get_available_providers():
        configured = config_manager.validate_provider_config(provider)
        status = "✓ Configured" if configured else "✗ Not configured"
        print(f"  {provider}: {status}")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
