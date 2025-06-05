"""
Ollama Provider Implementation
"""

import os
from typing import Dict, Any, List, Optional
from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage, SystemMessage, AIMessage

from .base import BaseLLMProvider, ChatMessage, ChatResponse


class OllamaProvider(BaseLLMProvider):
    """Ollama LLM Provider using LangChain"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.base_url = config.get('base_url', 'http://localhost:11434')
        self.default_model = config.get('default_model', 'llama2')
    
    def _create_client(self, model: str, temperature: float, max_tokens: Optional[int]) -> ChatOllama:
        """Create Ollama client with specified parameters"""
        return ChatOllama(
            model=model,
            temperature=temperature,
            num_predict=max_tokens,
            base_url=self.base_url
        )
    
    def _convert_messages(self, messages: List[ChatMessage]) -> List:
        """Convert ChatMessage objects to LangChain message format"""
        langchain_messages = []
        
        for msg in messages:
            if msg.role == 'system':
                langchain_messages.append(SystemMessage(content=msg.content))
            elif msg.role == 'user':
                langchain_messages.append(HumanMessage(content=msg.content))
            elif msg.role == 'assistant':
                langchain_messages.append(AIMessage(content=msg.content))
        
        return langchain_messages
    
    def chat_completion(
        self, 
        messages: List[ChatMessage], 
        model: str = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> ChatResponse:
        """Generate chat completion using Ollama"""
        try:
            model = model or self.default_model
            client = self._create_client(model, temperature, max_tokens)
            langchain_messages = self._convert_messages(messages)
            
            response = client.invoke(langchain_messages)
            
            return ChatResponse(
                content=response.content,
                model=model,
                provider='ollama',
                metadata={
                    'response_metadata': getattr(response, 'response_metadata', {}),
                    'usage_metadata': getattr(response, 'usage_metadata', {})
                }
            )
            
        except Exception as e:
            raise Exception(f"Ollama API error: {str(e)}")
    
    def get_available_models(self) -> List[str]:
        """Return list of common Ollama models"""
        return [
            'llama2',
            'llama2:13b',
            'llama2:70b',
            'mistral',
            'mixtral',
            'codellama',
            'phi',
            'neural-chat',
            'starling-lm'
        ]
    
    def validate_config(self) -> bool:
        """Validate Ollama configuration"""
        try:
            # Test with a simple request
            test_client = self._create_client(self.default_model, 0.1, 10)
            test_messages = [HumanMessage(content="Hi")]
            test_client.invoke(test_messages)
            return True
        except Exception:
            return False
