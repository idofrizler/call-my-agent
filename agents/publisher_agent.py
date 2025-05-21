"""Agent responsible for creating printable PDF layouts."""

from pathlib import Path
from semantic_kernel import Kernel
from semantic_kernel.functions.kernel_arguments import KernelArguments
from pydantic import BaseModel

from utils.pdf_generation import render_pdf
from .base_agent import BaseAgent

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

        # # Use model_dump() for Pydantic v2+ compatibility
        # if hasattr(data, "model_dump"):
        #     parsed = data.model_dump()
        # else:
        #     parsed = dict(data)

        # parsed = data.value[0].items[0].text.strip()
        logger.info(f"Extracted data: {data}")

        import ast
        parsed = ast.literal_eval(str(data))

        title = parsed.get("title")
        content = parsed.get("content")
        image_path = parsed.get("image_path")

        logger.info(f"Parsed data: {parsed}")
        logger.info(f"Title: {title}")
        logger.info(f"Content: {content}")
        logger.info(f"Image path: {image_path}")

        if not title or not content:
            return "Cannot generate PDF: title or content missing."

        args = { "title": title, "content": content }
        if image_path:
            args["image_path"] = image_path

        pdf_bytes = render_pdf(
            title=title,
            content=content,
            image_path=image_path or None
        )

        pdf_path = self.out_dir / "book.pdf"
        pdf_path.write_bytes(pdf_bytes)
        return f"PDF saved to {pdf_path}"
