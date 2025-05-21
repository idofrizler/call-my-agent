"""Illustrator agent implementation."""

from semantic_kernel import Kernel

from config import Config
from utils.image_generator import create_image
from .base_agent import BaseAgent

class IllustratorAgent(BaseAgent):
    """Agent responsible for generating and saving images."""

    def __init__(self, kernel: Kernel, cfg: Config):
        """Initialize the illustrator agent.
        
        Args:
            kernel: Semantic Kernel instance
            cfg: Application configuration
        """
        super().__init__(kernel, "IllustratorPlugin", "Illustrator")
        self.config = cfg

    async def respond(self, history: str) -> str:
        """Generate an image based on conversation history.
        
        Args:
            history: Chat history to process
            
        Returns:
            Markdown image reference, or just the prompt if generation fails
        """
        # Get prompt from base respond
        prompt = await super().respond(history)
        
        # Generate and save the image
        image_path = create_image(prompt, self.config)
        # image_path = "images\\20250521_155035.png"
        
        if image_path:
            # Return markdown referencing local file
            return f"![Generated illustration]({image_path} \"{prompt}\")"
        else:
            # Fall back to just the prompt on error
            return f"Failed to generate image for prompt: {prompt}"
