"""
OpenRouter Provider Implementation
"""

import os
from typing import Dict, Any, List, Optional
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage

from .base import BaseLLMProvider, ChatMessage, ChatResponse

class OpenRouterProvider(BaseLLMProvider):
    """OpenRouter LLM Provider using OpenAI-compatible API"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get('api_key') or os.getenv('OPENROUTER_API_KEY')
        self.base_url = config.get('base_url', 'https://openrouter.ai/api/v1')
        self.default_model = config.get('default_model', 'anthropic/claude-3.5-sonnet')
        if not self.api_key:
            raise ValueError("OpenRouter API key is required")

    def _create_client(self, model: str, temperature: float, max_tokens: Optional[int]) -> ChatOpenAI:
        return ChatOpenAI(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            openai_api_key=self.api_key,
            openai_api_base=self.base_url
        )

    def _convert_messages(self, messages: List[ChatMessage]) -> List:
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
        try:
            model = model or self.default_model
            client = self._create_client(model, temperature, max_tokens)
            langchain_messages = self._convert_messages(messages)
            response = client.invoke(langchain_messages)
            return ChatResponse(
                content=response.content,
                model=model,
                provider='openrouter',
                metadata={
                    'response_metadata': getattr(response, 'response_metadata', {}),
                    'usage_metadata': getattr(response, 'usage_metadata', {})
                }
            )
        except Exception as e:
            raise Exception(f"OpenRouter API error: {str(e)}")

    def get_available_models(self) -> List[str]:
        return [
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

    def validate_config(self) -> bool:
        if not self.api_key:
            return False
        try:
            test_client = self._create_client(self.default_model, 0.1, 10)
            test_messages = [HumanMessage(content="Hi")]
            test_client.invoke(test_messages)
            return True
        except Exception:
            return False
