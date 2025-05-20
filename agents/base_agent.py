"""Base class for all agents."""

from abc import ABC, abstractmethod

from semantic_kernel import Kernel
from semantic_kernel.functions import KernelArguments

class BaseAgent(ABC):
    """Abstract base class for story-creation agents."""

    def __init__(self, kernel: Kernel, plugin_name: str, function_name: str):
        """Initialize the agent.
        
        Args:
            kernel: Semantic Kernel instance
            plugin_name: Name of the plugin to use
            function_name: Name of the function to call
        """
        self.kernel = kernel
        self.plugin_name = plugin_name
        self.function_name = function_name

    async def respond(self, history: str) -> str:
        """Generate a response based on conversation history.
        
        Args:
            history: Chat history to process
            
        Returns:
            Agent's response
        """
        plugin = self.kernel.plugins[self.plugin_name]
        function = plugin.functions[self.function_name]
        response = await self.kernel.invoke(
            function,
            KernelArguments(history=history)
        )
        return response.value[0].content.strip()
