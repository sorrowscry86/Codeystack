"""
LLM Configuration Management
Handles configuration for different LLM providers
"""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class LLMConfig:
    """Configuration for LLM providers"""
    provider: str
    model: str
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    additional_params: Optional[Dict[str, Any]] = None


class LLMConfigManager:
    """Manages LLM provider configurations"""
    
    def __init__(self):
        self.configs = {}
        self._load_default_configs()
    
    def _load_default_configs(self):
        """Load default configurations for all providers"""
        self.configs = {
            'openai': {
                'api_key': os.getenv('OPENAI_API_KEY'),
                'base_url': 'https://api.openai.com/v1',
                'default_model': 'gpt-3.5-turbo',
                'available_models': [
                    'gpt-4',
                    'gpt-4-turbo',
                    'gpt-4-turbo-preview',
                    'gpt-3.5-turbo',
                    'gpt-3.5-turbo-16k'
                ]
            },
            'anthropic': {
                'api_key': os.getenv('ANTHROPIC_API_KEY'),
                'default_model': 'claude-3-sonnet-20240229',
                'available_models': [
                    'claude-3-opus-20240229',
                    'claude-3-sonnet-20240229',
                    'claude-3-haiku-20240307',
                    'claude-2.1',
                    'claude-2.0'
                ]
            },
            'google': {
                'api_key': os.getenv('GEMINI_API_KEY'),  # Corrected to GEMINI_API_KEY
                'default_model': 'gemini-1.5-flash',  # Updated default model to a valid one
                'available_models': [
                    'gemini-pro',
                    'gemini-pro-vision',
                    'gemini-1.5-pro',
                    'gemini-1.5-flash'
                ]
            },
            'openrouter': {
                'api_key': os.getenv('OPENROUTER_API_KEY'),
                'base_url': 'https://openrouter.ai/api/v1',
                'default_model': 'anthropic/claude-3.5-sonnet',
                'available_models': [
                    'anthropic/claude-3.5-sonnet',
                    'openai/gpt-4o',
                    'meta-llama/llama-3.1-70b-instruct',
                    'deepseek/deepseek-r1-0528:free',
                    'google/gemini-pro',
                    'mistralai/mixtral-8x22b-instruct',
                    'meta-llama/llama-2-70b-chat',
                    'openrouter/cinematika-7b',
                    'openrouter/auto',
                ]
            },
            'ollama': {
                'base_url': os.getenv('OLLAMA_BASE_URL', 'http://host.docker.internal:11434'),
                'default_model': 'llama3.1:latest',
                'available_models': [
                    'llama3.1:latest',
                    'deepseek-r1:latest',
                    'qwen3:latest',
                    'llama3.2:1b',
                    'llama2',
                    'llama2:13b',
                    'llama2:70b',
                    'mistral',
                    'mixtral',
                    'codellama'
                ]
            }
        }
    
    def get_config(self, provider: str) -> Dict[str, Any]:
        """Get configuration for a specific provider"""
        return self.configs.get(provider.lower(), {})
    
    def update_config(self, provider: str, config: Dict[str, Any]):
        """Update configuration for a specific provider"""
        provider = provider.lower()
        if provider not in self.configs:
            self.configs[provider] = {}
        self.configs[provider].update(config)
    
    def set_api_key(self, provider: str, api_key: str):
        """Set API key for a specific provider"""
        provider = provider.lower()
        if provider not in self.configs:
            self.configs[provider] = {}
        self.configs[provider]['api_key'] = api_key
    
    def get_available_providers(self) -> list[str]:
        """Get list of available providers"""
        return list(self.configs.keys())
    
    def validate_provider_config(self, provider: str) -> bool:
        """Validate if provider configuration is complete"""
        config = self.get_config(provider)
        
        if provider in ['openai', 'anthropic', 'google']:
            return bool(config.get('api_key'))
        elif provider == 'ollama':
            return bool(config.get('base_url'))
        
        return False
    
    def create_llm_config(
        self,
        provider: str,
        model: str = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMConfig:
        """Create an LLMConfig object"""
        config = self.get_config(provider)
        
        return LLMConfig(
            provider=provider,
            model=model or config.get('default_model'),
            temperature=temperature,
            max_tokens=max_tokens,
            api_key=config.get('api_key'),
            base_url=config.get('base_url'),
            additional_params=kwargs
        )
