from .base import BaseAIService
from .deepseek import DeepSeekService
from .qwen import QwenService


def get_ai_service(provider: str = "deepseek") -> BaseAIService:
    if provider == "qwen":
        return QwenService()
    return DeepSeekService()
