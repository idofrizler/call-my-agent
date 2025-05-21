"""Illustrator agent implementation."""

from semantic_kernel import Kernel

from .base_agent import BaseAgent

class IllustratorAgent(BaseAgent):
    """Agent responsible for generating image descriptions."""

    def __init__(self, kernel: Kernel):
        """Initialize the illustrator agent.
        
        Args:
            kernel: Semantic Kernel instance
        """
        super().__init__(kernel, "IllustratorPlugin", "Illustrator")
