"""Writer agent implementation."""

from semantic_kernel import Kernel

from .base_agent import BaseAgent

class WriterAgent(BaseAgent):
    """Agent responsible for writing story content and titles."""

    def __init__(self, kernel: Kernel):
        """Initialize the writer agent.
        
        Args:
            kernel: Semantic Kernel instance
        """
        super().__init__(kernel, "WriterPlugin", "WriteContent")

    def _pick_function(self, last_line: str) -> str:
        """Choose whether to generate a title or content based on user's request.
        
        Args:
            last_line: Last line from conversation history
            
        Returns:
            Name of function to call ('SuggestTitle' or 'WriteContent')
        """
        lowered = last_line.lower()
        if "title" in lowered and "content" not in lowered:
            return "SuggestTitle"
        return "WriteContent"

    async def respond(self, history: str) -> str:
        """Generate a response based on conversation history.
        
        Args:
            history: Chat history to process
            
        Returns:
            Agent's response (either a title or story content)
        """
        # Get the last line from history to determine function
        lines = history.strip().splitlines()
        if not lines:
            return await super().respond(history)
            
        # Pick appropriate function based on last line
        self.function_name = self._pick_function(lines[-1])
        return await super().respond(history)
