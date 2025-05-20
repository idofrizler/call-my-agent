"""Writer agent implementation."""

from semantic_kernel import Kernel

from .base_agent import BaseAgent

class WriterAgent(BaseAgent):
    """Agent responsible for writing story content."""

    def __init__(self, kernel: Kernel):
        """Initialize the writer agent.
        
        Args:
            kernel: Semantic Kernel instance
        """
        super().__init__(kernel, "WriterPlugin", "Writer")
