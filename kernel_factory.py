"""Factory for creating and configuring Semantic Kernel instances."""

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

from config import Config

def build_kernel(cfg: Config) -> Kernel:
    """Create and configure a new Semantic Kernel instance.
    
    Args:
        cfg: Application configuration containing Azure OpenAI settings
        
    Returns:
        Configured Semantic Kernel instance
    """
    kernel = Kernel()
    
    chat_service = AzureChatCompletion(
        deployment_name=cfg.deployment,
        endpoint=cfg.endpoint,
        api_key=cfg.api_key,
        api_version=cfg.api_version,
    )
    
    kernel.add_service(chat_service)
    return kernel
