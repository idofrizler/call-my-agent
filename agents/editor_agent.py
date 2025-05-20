"""Editor agent implementation."""

from semantic_kernel import Kernel

from .base_agent import BaseAgent

class EditorAgent(BaseAgent):
    """Agent responsible for reviewing story content."""

    def __init__(self, kernel: Kernel):
        """Initialize the editor agent.
        
        Args:
            kernel: Semantic Kernel instance
        """
        super().__init__(kernel, "EditorPlugin", "Editor")
    
    def is_ready(self, response: str) -> bool:
        """Check if the editor thinks the book is ready.
        
        Args:
            response: Editor's response to check
            
        Returns:
            True if the book is ready to publish
        """
        return "The book is ready" in response
