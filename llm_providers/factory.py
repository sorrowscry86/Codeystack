"""
LLM Provider Factory
Central factory for creating and managing LLM providers
"""

from typing import Dict, Any, Type
from .base import BaseLLMProvider
from .openai_provider import OpenAIProvider
from .anthropic_provider import AnthropicProvider
from .google_provider import GoogleProvider
from .ollama_provider import OllamaProvider
from .openrouter_provider import OpenRouterProvider
from .lmstudio_provider import LMStudioProvider
from .koboldcpp_provider import KoboldCppProvider


class LLMProviderFactory:
    """Factory class for creating LLM providers"""
    
    _providers: Dict[str, Type[BaseLLMProvider]] = {
        'openai': OpenAIProvider,
        'anthropic': AnthropicProvider,
        'google': GoogleProvider,
        'ollama': OllamaProvider,
        'openrouter': OpenRouterProvider,
        'lmstudio': LMStudioProvider,
        'koboldcpp': KoboldCppProvider
    }
    
    @classmethod
    def create_provider(cls, provider_name: str, config: Dict[str, Any]) -> BaseLLMProvider:
        """
        Create an LLM provider instance
        
        Args:
            provider_name: Name of the provider ('openai', 'anthropic', 'google', 'ollama')
            config: Configuration dictionary for the provider
            
        Returns:
            BaseLLMProvider instance
            
        Raises:
            ValueError: If provider_name is not supported
        """
        provider_name = provider_name.lower()
        
        if provider_name not in cls._providers:
            available_providers = ', '.join(cls._providers.keys())
            raise ValueError(f"Unsupported provider: {provider_name}. Available providers: {available_providers}")
        
        provider_class = cls._providers[provider_name]
        return provider_class(config)
    
    @classmethod
    def get_available_providers(cls) -> list[str]:
        """Get list of available provider names"""
        return list(cls._providers.keys())
    
    @classmethod
    def register_provider(cls, name: str, provider_class: Type[BaseLLMProvider]):
        """Register a new provider class"""
        cls._providers[name.lower()] = provider_class
