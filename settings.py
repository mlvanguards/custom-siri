from pathlib import Path
from typing import ClassVar, Optional

from pydantic_settings import BaseSettings


class BaseAppSettings(BaseSettings):
    """Base settings class with common configuration."""

    BASE_DIR: ClassVar[Path] = Path(__file__).resolve().parent.parent.parent

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


class AuthSettings(BaseAppSettings):
    """Authentication and API keys settings."""

    HUGGINGFACE_TOKEN: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None


class DatasetSettings(BaseAppSettings):
    """LLM settings for dataset generation."""

    # Ollama configuration  
    LLM_MODEL: str = "ollama/llama3.1:8b"  # Use Ollama with Llama 3.1 8B (smarter, good with 16GB RAM)
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    
    # Alternative models you can use:
    # "ollama/llama3.1:8b" - Llama 3.1 8B
    # "ollama/gemma2:9b" - Gemma 2 9B  
    # "ollama/llama3.2:3b" - Llama 3.2 3B (smaller, faster)
    # "ollama/qwen2.5:7b" - Qwen 2.5 7B
    
    # Dataset generation parameters
    SINGLE_TOOL_EXAMPLES_PER_TOOL: int = 2
    MULTI_TOOL_EXAMPLES: int = 2
    UNKNOWN_INTENT_EXAMPLES: int = 2
    PARAPHRASE_COUNT: int = 2


class Settings(BaseAppSettings):
    """Main settings class that combines all specialized settings."""

    auth: AuthSettings = AuthSettings()
    dataset: DatasetSettings = DatasetSettings()


# Create global settings instance
settings = Settings()
