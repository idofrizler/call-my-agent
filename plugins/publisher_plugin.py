"""Publisher plugin: lay out title, content and illustration, output A4 PDF."""

import io
import textwrap
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from semantic_kernel.functions import KernelPlugin, KernelFunction, kernel_function


@kernel_function
def _render_pdf(title: str, content: str, image_path: str|None=None) -> bytes:
    """Create PDF with title, optional image, and wrapped text content.
    
    Args:
        title: Book/chapter title
        content: Main text content
        image_path: Optional path to illustration image
        
    Returns:
        PDF file contents as bytes
    """
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    w, h = A4
    margin = 2*cm

    # Title
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(w/2, h-margin, title)
    y = h - margin - 2*cm

    # Illustration (if provided)
    if image_path:
        img = ImageReader(image_path)
        img_w, img_h = img.getSize()
        scale = (w-2*margin) / img_w
        img_h_scaled = img_h * scale
        c.drawImage(img, margin, y-img_h_scaled, width=w-2*margin, height=img_h_scaled, 
                   preserveAspectRatio=True, anchor="n")
        y -= img_h_scaled + 1*cm

    # Body text with simple wrapping
    c.setFont("Times-Roman", 12)
    for line in textwrap.wrap(content, width=90):
        if y < margin+1*cm:  # Start new page if needed
            c.showPage()
            y = h - margin
            c.setFont("Times-Roman", 12)
        c.drawString(margin, y, line)
        y -= 0.6*cm

    c.save()
    return buf.getvalue()

def build_publisher_plugin() -> KernelPlugin:
    """Create and configure the publisher plugin.
    
    Returns:
        Configured KernelPlugin for the publisher role
    """
    pub_fn = KernelFunction.from_method(
        plugin_name="PublisherPlugin",
        # function_name="Publish",
        # description="Return printable PDF bytes from title/content/image",
        method=_render_pdf,
    )
    return KernelPlugin(name="PublisherPlugin", functions=[pub_fn])
