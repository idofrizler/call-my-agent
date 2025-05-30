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
    image_paths: list[str] = []


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
        # Handle both new image_paths and legacy image_path
        image_paths = parsed.get("image_paths", [])
        if not image_paths and parsed.get("image_path"):
            image_paths = [parsed["image_path"]]

        logger.info(f"Parsed data: {parsed}")
        logger.info(f"Title: {title}")
        logger.info(f"Content: {content}")
        logger.info(f"Image paths: {image_paths}")

        if not title or not content:
            return "Cannot generate PDF: title or content missing."

        # Convert image paths to image blocks with full width and no captions
        image_blocks = [{"path": path, "full_width": True} for path in image_paths] if image_paths else None
        
        pdf_bytes = render_pdf(
            title=title,
            content=content,
            image_blocks=image_blocks
        )

        from datetime import datetime

        # add title and timestamp to filename
        filename = f"{title.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf_path = self.out_dir / filename
        pdf_path.write_bytes(pdf_bytes)
        return f"PDF saved to {pdf_path}"
