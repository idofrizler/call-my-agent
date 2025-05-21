"""Agent responsible for creating printable PDF layouts."""

from pathlib import Path
from semantic_kernel import Kernel
from semantic_kernel.functions.kernel_arguments import KernelArguments

from .base_agent import BaseAgent


class PublisherAgent(BaseAgent):
    """Agent that calls PublisherPlugin.Publish to generate PDFs."""

    def __init__(self, kernel: Kernel, output_dir: str = "output"):
        """Initialize the publisher agent.
        
        Args:
            kernel: Semantic Kernel instance
            output_dir: Directory to save PDF files (default: "output")
        """
        super().__init__(kernel, "PublisherPlugin", "Publish")
        self.out_dir = Path(output_dir)
        self.out_dir.mkdir(exist_ok=True)

    async def respond(self, history: str) -> str:
        title = self._extract("title:", history)
        content = self._extract("content:", history)
        image_path = self._extract("image:", history)

        if not title or not content:
            return "Cannot generate PDF: title or content missing."

        args = { "title": title, "content": content }
        if image_path:
            args["image_path"] = image_path

        pdf_bytes = await self.kernel.invoke(
            self.kernel.plugins["PublisherPlugin"].functions["_render_pdf"],
            KernelArguments(args)
        )

        pdf_path = self.out_dir / "book.pdf"
        pdf_path.write_bytes(pdf_bytes.value)
        return f"PDF saved to {pdf_path}"


    @staticmethod
    def _extract(key: str, text: str) -> str:
        """Extract the value following a key from text.
        
        Searches backwards through lines to find most recent occurrence.
        
        Args:
            key: Key to search for (e.g. "title:")
            text: Text to search in
            
        Returns:
            Extracted value or empty string if not found
        """
        for line in reversed(text.splitlines()):
            if line.lower().startswith(key):
                return line[len(key):].strip()
        return ""
