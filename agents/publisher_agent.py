"""Agent responsible for creating printable PDF layouts."""

from pathlib import Path
from semantic_kernel import Kernel
from semantic_kernel.functions.kernel_arguments import KernelArguments
from pydantic import BaseModel

from .base_agent import BaseAgent


class PublisherOutput(BaseModel):
    title: str
    content: str
    image_path: str = ""


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

    async def _extract_structured(self, history: str) -> PublisherOutput:
        """Use plugin function to extract title, content, and image_path as structured JSON from history, validated by PublisherOutput."""
        result = await self.kernel.invoke(
            self.kernel.plugins["PublisherPlugin"].functions["extract_structured"],
            KernelArguments(input=history),
            output_type=PublisherOutput
        )
        return result

    async def respond(self, history: str) -> str:
        data = await self._extract_structured(history)
        title = data.title
        content = data.content
        image_path = data.image_path

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
