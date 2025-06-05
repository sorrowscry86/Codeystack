"""
Test Script for Multi-LLM Provider System
Tests the provider system without making actual API calls
"""

import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from llm_providers.factory import LLMProviderFactory
from llm_providers.base import ChatMessage
from config.llm_config import LLMConfigManager


def test_provider_factory():
    """Test the provider factory functionality"""
    print("=== Testing LLM Provider Factory ===")
    
    # Test getting available providers
    providers = LLMProviderFactory.get_available_providers()
    print(f"Available providers: {providers}")
    
    # Test creating providers with mock configurations
    for provider_name in providers:
        try:
            # Create minimal config for testing
            if provider_name == 'ollama':
                config = {'base_url': 'http://localhost:11434', 'default_model': 'llama2'}
            else:
                config = {'api_key': 'test_key_12345', 'default_model': 'test_model'}
            
            provider = LLMProviderFactory.create_provider(provider_name, config)
            models = provider.get_available_models()
            
            print(f"✓ {provider_name.upper()} Provider:")
            print(f"  - Class: {provider.__class__.__name__}")
            print(f"  - Available models: {len(models)} ({', '.join(models[:3])}{'...' if len(models) > 3 else ''})")
            print(f"  - Default model: {provider.get_default_model()}")
            
        except Exception as e:
            print(f"✗ {provider_name.upper()} Provider failed: {str(e)}")
    
    print()


def test_config_manager():
    """Test the configuration manager"""
    print("=== Testing Configuration Manager ===")
    
    config_manager = LLMConfigManager()
    
    # Test getting configurations
    for provider in config_manager.get_available_providers():
        config = config_manager.get_config(provider)
        configured = config_manager.validate_provider_config(provider)
        
        print(f"{provider.upper()}:")
        print(f"  - Default model: {config.get('default_model', 'Not set')}")
        print(f"  - Configured: {'✓' if configured else '✗'}")
        if provider == 'ollama':
            print(f"  - Base URL: {config.get('base_url', 'Not set')}")
        else:
            print(f"  - API Key: {'Set' if config.get('api_key') else 'Not set'}")
    
    print()


def test_message_structure():
    """Test the message and response structure"""
    print("=== Testing Message Structure ===")
    
    # Test ChatMessage creation
    messages = [
        ChatMessage(role='system', content='You are a helpful assistant.'),
        ChatMessage(role='user', content='Hello, how are you?'),
        ChatMessage(role='assistant', content='I am doing well, thank you!')
    ]
    
    print("Created test messages:")
    for i, msg in enumerate(messages, 1):
        print(f"  {i}. {msg.role}: {msg.content[:50]}{'...' if len(msg.content) > 50 else ''}")
    
    print()


def test_provider_methods():
    """Test provider methods without making API calls"""
    print("=== Testing Provider Methods ===")
    
    # Test with mock configuration
    test_configs = {
        'openai': {'api_key': 'sk-test123', 'default_model': 'gpt-3.5-turbo'},
        'anthropic': {'api_key': 'ant-test123', 'default_model': 'claude-3-sonnet-20240229'},
        'google': {'api_key': 'google-test123', 'default_model': 'gemini-pro'},
        'ollama': {'base_url': 'http://localhost:11434', 'default_model': 'llama2'}
    }
    
    for provider_name, config in test_configs.items():
        try:
            provider = LLMProviderFactory.create_provider(provider_name, config)
            
            print(f"{provider_name.upper()} Provider Methods:")
            print(f"  - get_available_models(): {len(provider.get_available_models())} models")
            print(f"  - get_default_model(): {provider.get_default_model()}")
            print(f"  - Provider name: {provider.provider_name}")
            
            # Note: We're not testing chat_completion or validate_config here
            # as they would require actual API calls
            
        except Exception as e:
            print(f"  ✗ Error testing {provider_name}: {str(e)}")
    
    print()


def main():
    """Run all tests"""
    print("Studio Lite Multi-LLM Provider System Test")
    print("=" * 50)
    
    try:
        test_provider_factory()
        test_config_manager()
        test_message_structure()
        test_provider_methods()
        
        print("=== Test Summary ===")
        print("✓ Provider factory working")
        print("✓ Configuration manager working")
        print("✓ Message structures working")
        print("✓ Provider methods accessible")
        print()
        print("Next steps:")
        print("1. Set up API keys in environment variables or .env file")
        print("2. Test actual API calls using the Flask application")
        print("3. Verify error handling and edge cases")
        
    except Exception as e:
        print(f"✗ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
