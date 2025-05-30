"""Configuration management for Call My Agent."""

from dataclasses import dataclass
import os
from typing import Optional

from dotenv import load_dotenv

@dataclass
class Config:
    """Application configuration loaded from environment variables."""
    
    api_key: str
    endpoint: str
    deployment: str  # GPT deployment for chat
    image_deployment: str  # DALL-E deployment for images
    model: str
    api_version: str
    image_api_version: str
    max_turns: int = 20
    
    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables."""
        load_dotenv()

        required = {
            "api_key": "AZURE_OPENAI_API_KEY",
            "endpoint": "AZURE_OPENAI_ENDPOINT", 
            "deployment": "AZURE_OPENAI_DEPLOYMENT",  # GPT deployment for chat
            "image_deployment": "AZURE_OPENAI_IMAGE_DEPLOYMENT",  # DALL-E deployment for images
            "model": "AZURE_OPENAI_MODEL",
            "api_version": "AZURE_OPENAI_API_VERSION",  # Should be recent enough for DALL-E (e.g. 2024-02-15-preview)
            "image_api_version": "AZURE_OPENAI_IMAGE_API_VERSION",  # Should be recent enough for DALL-E (e.g. 2024-02-15-preview)
        }

        missing = [env for env in required.values() if not os.getenv(env)]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

        return cls(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            image_deployment=os.getenv("AZURE_OPENAI_IMAGE_DEPLOYMENT"),
            model=os.getenv("AZURE_OPENAI_MODEL"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            image_api_version=os.getenv("AZURE_OPENAI_IMAGE_API_VERSION"),
            max_turns=int(os.getenv("MAX_TURNS", "20")),
        )
