"""
Base LLM Provider Interface
Defines the common interface that all LLM providers must implement
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class ChatMessage:
    """Represents a chat message"""
    role: str  # 'user', 'assistant', 'system'
    content: str


@dataclass
class ChatResponse:
    """Represents a chat response from an LLM provider"""
    content: str
    model: str
    provider: str
    usage: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


class BaseLLMProvider(ABC):
    """Abstract base class for all LLM providers"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.provider_name = self.__class__.__name__.replace('Provider', '').lower()
    
    @abstractmethod
    def chat_completion(
        self, 
        messages: List[ChatMessage], 
        model: str = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> ChatResponse:
        """
        Generate a chat completion response
        
        Args:
            messages: List of chat messages
            model: Model name to use (if None, uses default)
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional provider-specific parameters
            
        Returns:
            ChatResponse object with the generated response
        """
        pass
    
    @abstractmethod
    def get_available_models(self) -> List[str]:
        """Return list of available models for this provider"""
        pass
    
    @abstractmethod
    def validate_config(self) -> bool:
        """Validate the provider configuration"""
        pass
    
    def get_default_model(self) -> str:
        """Get the default model for this provider"""
        models = self.get_available_models()
        return models[0] if models else None
