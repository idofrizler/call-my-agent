"""Editor agent implementation."""

from semantic_kernel import Kernel

from .base_agent import BaseAgent

class EditorAgent(BaseAgent):
    """Agent responsible for reviewing story content and requesting illustrations."""

    def __init__(self, kernel: Kernel):
        """Initialize the editor agent.
        
        Args:
            kernel: Semantic Kernel instance
        """
        super().__init__(kernel, "EditorPlugin", "Editor")
        self.image_queue = []  # Stores pending image prompts
        self.text_ready = False  # Tracks if text content is approved
    
    def is_ready(self) -> bool:
        """Check if the book is ready for publication.
        
        Returns:
            True if text is approved and all requested images are complete
        """
        return self.text_ready and not self.image_queue

    async def respond(self, history: str) -> str:
        """Process editor response and update internal state.
        
        Args:
            history: Chat history to process
            
        Returns:
            Editor's formatted response
        """
        response = await super().respond(history)
        
        # Parse image requests and text approval
        self.image_queue = []
        self.text_ready = False
        
        for line in response.split('\n'):
            if line.strip().startswith('IMG:'):
                # Extract image prompt after IMG: prefix
                prompt = line.strip()[4:].strip()
                if prompt:
                    self.image_queue.append(prompt)
            elif "The book is ready" in line:
                self.text_ready = True
        
        return response
