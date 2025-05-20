"""Selector agent implementation."""

from semantic_kernel import Kernel

from .base_agent import BaseAgent

class SelectorAgent(BaseAgent):
    """Agent responsible for choosing the next agent to respond."""

    def __init__(self, kernel: Kernel):
        """Initialize the selector agent.
        
        Args:
            kernel: Semantic Kernel instance
        """
        super().__init__(kernel, "SelectorPlugin", "Selector")

    async def next(self, history: str) -> str:
        """Decide which agent should respond next.
        
        Args:
            history: Chat history to analyze
            
        Returns:
            Name of the next agent ('Writer' or 'Editor')
        """
        response = await self.respond(history)
        
        # Validate and normalize response
        agent = response.strip()
        if agent not in ["Writer", "Editor"]:
            return "Writer"  # Default to writer if invalid response
            
        return agent
