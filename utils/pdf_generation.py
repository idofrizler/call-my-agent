"""PDF generation utilities."""

import io
import textwrap
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

def render_pdf(title: str, content: str, image_path: str|None=None) -> bytes:
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
