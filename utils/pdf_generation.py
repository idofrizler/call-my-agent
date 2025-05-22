"""PDF generation utilities with professional layout."""

import io
from typing import Optional, Dict, List

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer, PageBreak, KeepTogether
from reportlab.platypus.frames import Frame
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate

class BookPDF(BaseDocTemplate):
    """Custom document template with headers and footers."""
    
    def __init__(self, buffer, book_title: str, **kwargs):
        super().__init__(buffer, **kwargs)
        self.book_title = book_title
        self.page_count = 0
        
    def afterPage(self):
        """Track page count for footer."""
        self.page_count += 1
        
    def header_footer(self, canvas, doc):
        """Draw headers and footers on each page."""
        canvas.saveState()
        
        # Header - book title on left
        canvas.setFont('Times-Roman', 9)
        canvas.drawString(doc.leftMargin, doc.pagesize[1] - 0.75*cm, self.book_title)
        
        # Footer - centered page number
        canvas.setFont('Times-Roman', 9)
        page_num = f"- {self.page_count} -"
        canvas.drawCentredString(doc.pagesize[0]/2, 1*cm, page_num)
        
        canvas.restoreState()

def render_pdf(
    title: str, 
    content: str,
    image_blocks: Optional[List[Dict[str, str]]] = None,
    layout: str = "single"
) -> bytes:
    """Create PDF with professional layout including images and text flow.
    
    Args:
        title: Book/chapter title
        content: Main text content
        image_blocks: Optional list of dicts with keys:
            - path: Path to image file
            - caption: Optional caption text
            - full_width: If False, allows text to flow beside image
        layout: "single" or "two_column"
        
    Returns:
        PDF file contents as bytes
    """
    # Setup document
    buf = io.BytesIO()
    doc = BookPDF(
        buf,
        title,
        pagesize=A4,
        leftMargin=2*cm,
        rightMargin=2*cm,
        topMargin=2.5*cm,
        bottomMargin=2*cm,
    )
    
    # Configure page template with header/footer
    frame = Frame(
        doc.leftMargin,
        doc.bottomMargin,
        doc.width,
        doc.height,
        leftPadding=0,
        rightPadding=0,
        bottomPadding=0,
        topPadding=0,
    )
    template = PageTemplate(
        'normal',
        [frame],
        onPage=doc.header_footer
    )
    doc.addPageTemplates([template])
    
    # Setup styles
    styles = getSampleStyleSheet()
    
    # Modify existing Title style instead of adding new one
    styles['Title'].fontSize = 20
    styles['Title'].spaceAfter = 12
    styles['Title'].alignment = TA_CENTER
    
    # Add custom styles
    styles.add(
        ParagraphStyle(
            name='BookBody',
            parent=styles['Normal'],
            fontName='Times-Roman',
            fontSize=11,
            leading=14,
            alignment=TA_JUSTIFY,
            firstLineIndent=0.5*cm,
            spaceBefore=6,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name='BookCaption',
            parent=styles['Normal'],
            fontName='Times-Italic',
            fontSize=9,
            leading=11,
            alignment=TA_CENTER,
            spaceBefore=4,
            spaceAfter=12,
        )
    )
    
    # Build content
    story = []
    
    # Title
    story.append(Paragraph(title, styles['Title']))
    story.append(Spacer(1, 0.5*cm))
    
    # Split content into paragraphs and convert to Platypus flowables
    paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
    
    # If images provided, interleave with paragraphs
    if image_blocks:
        para_idx = 0
        img_idx = 0
        while para_idx < len(paragraphs) or img_idx < len(image_blocks):
            # Add next paragraph if available and appropriate
            if para_idx < len(paragraphs) and (
                img_idx >= len(image_blocks) or 
                para_idx <= img_idx * 3  # Rough spacing of images
            ):
                story.append(Paragraph(paragraphs[para_idx], styles['BookBody']))
                para_idx += 1
            
            # Add next image if available
            if img_idx < len(image_blocks):
                img_block = image_blocks[img_idx]
                # Get natural image size from PIL
                from PIL import Image as PILImage
                pil_img = PILImage.open(img_block['path'])
                img_w, img_h = pil_img.size
                
                # Calculate dimensions preserving aspect ratio
                img_width = doc.width if img_block.get('full_width', True) else doc.width*0.5
                aspect = img_h / img_w
                img_height = img_width * aspect
                
                # Create ReportLab image with calculated dimensions
                img = Image(img_block['path'], width=img_width, height=img_height)
                
                elements = [img]
                if img_block.get('caption'):
                    elements.append(Paragraph(img_block['caption'], styles['BookCaption']))
                
                story.append(KeepTogether(elements))
                story.append(Spacer(1, 0.3*cm))
                img_idx += 1
    else:
        # Just process all paragraphs
        for para in paragraphs:
            story.append(Paragraph(para, styles['BookBody']))
    
    # Build PDF
    doc.build(story)
    return buf.getvalue()
