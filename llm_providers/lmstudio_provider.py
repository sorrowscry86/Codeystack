"""
LM Studio Provider Implementation
"""

from typing import Dict, Any, List, Optional

from .base import BaseLLMProvider, ChatMessage, ChatResponse

class LMStudioProvider(BaseLLMProvider):
    """LM Studio LLM Provider"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.base_url = config.get('base_url', 'http://localhost:5000')
        self.default_model = config.get('default_model', 'default')

    def _create_client(self, model: str, temperature: float, max_tokens: Optional[int]) -> Any:
        """Create LM Studio client with specified parameters"""
        return {
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "base_url": self.base_url
        }

    def _convert_messages(self, messages: List[ChatMessage]) -> List:
        """Convert ChatMessage objects to LM Studio message format"""
        return [
            {"role": msg.role, "content": msg.content} for msg in messages
        ]

    def chat_completion(
        self, 
        messages: List[ChatMessage], 
        model: str = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> ChatResponse:
        """Generate chat completion using LM Studio"""
        try:
            model = model or self.default_model
            client = self._create_client(model, temperature, max_tokens)
            converted_messages = self._convert_messages(messages)

            # Simulate API call
            response = {
                "content": "Simulated response from LM Studio",
                "model": model,
                "provider": "lmstudio",
                "metadata": {}
            }

            return ChatResponse(
                content=response["content"],
                model=response["model"],
                provider=response["provider"],
                metadata=response["metadata"]
            )
        except Exception as e:
            raise Exception(f"LM Studio API error: {str(e)}")

    def get_available_models(self) -> List[str]:
        """Return list of available LM Studio models"""
        return ["default", "model-a", "model-b"]

    def validate_config(self) -> bool:
        """Validate LM Studio configuration"""
        return bool(self.base_url)