"""
PDF Editing Services
Handles rotation, watermarks, page numbers, cropping, etc.
"""

import os
import logging
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image

logger = logging.getLogger(__name__)


async def rotate_pdf(pdf_path: str, rotation: int, output_path: str = None) -> str:
    """
    Rotate all pages in a PDF
    
    Args:
        pdf_path: Path to input PDF
        rotation: Rotation angle (90, 180, 270)
        output_path: Output PDF path (optional)
        
    Returns:
        Path to output PDF
    """
    try:
        if rotation not in [90, 180, 270]:
            raise ValueError("Rotation must be 90, 180, or 270 degrees")
        
        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        
        for page in reader.pages:
            rotated_page = page.rotate(rotation)
            writer.add_page(rotated_page)
        
        if not output_path:
            output_path = pdf_path.rsplit('.', 1)[0] + '_rotated.pdf'
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        logger.info(f"Rotated PDF saved to: {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Error rotating PDF: {e}")
        raise


async def add_watermark(pdf_path: str, watermark_path: str, output_path: str = None) -> str:
    """
    Add a watermark image to all pages of a PDF
    
    Args:
        pdf_path: Path to input PDF
        watermark_path: Path to watermark image
        output_path: Output PDF path (optional)
        
    Returns:
        Path to output PDF
    """
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        from io import BytesIO
        
        # Create watermark PDF
        watermark_pdf = BytesIO()
        c = canvas.Canvas(watermark_pdf, pagesize=letter)
        
        # Get watermark image dimensions
        img = Image.open(watermark_path)
        img_width, img_height = img.size
        
        # Scale watermark if too large
        page_width, page_height = letter
        if img_width > page_width * 0.5 or img_height > page_height * 0.5:
            scale = min(page_width * 0.5 / img_width, page_height * 0.5 / img_height)
            img_width = int(img_width * scale)
            img_height = int(img_height * scale)
        
        # Center watermark
        x = (page_width - img_width) / 2
        y = (page_height - img_height) / 2
        
        c.drawImage(watermark_path, x, y, width=img_width, height=img_height, mask='auto')
        c.save()
        watermark_pdf.seek(0)
        
        # Apply watermark to all pages
        reader = PdfReader(pdf_path)
        watermark_reader = PdfReader(watermark_pdf)
        watermark_page = watermark_reader.pages[0]
        
        writer = PdfWriter()
        for page in reader.pages:
            page.merge_page(watermark_page)
            writer.add_page(page)
        
        if not output_path:
            output_path = pdf_path.rsplit('.', 1)[0] + '_watermarked.pdf'
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        logger.info(f"Watermarked PDF saved to: {output_path}")
        return output_path
        
    except ImportError:
        logger.error("reportlab not installed. Install with: pip install reportlab")
        raise
    except Exception as e:
        logger.error(f"Error adding watermark: {e}")
        raise


async def add_page_numbers(pdf_path: str, output_path: str = None, 
                          position: str = 'bottom-right') -> str:
    """
    Add page numbers to all pages of a PDF
    
    Args:
        pdf_path: Path to input PDF
        output_path: Output PDF path (optional)
        position: Position of page numbers ('bottom-right', 'bottom-center', etc.)
        
    Returns:
        Path to output PDF
    """
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        from io import BytesIO
        
        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        
        for page_num, page in enumerate(reader.pages, 1):
            # Create page number overlay
            overlay_pdf = BytesIO()
            c = canvas.Canvas(overlay_pdf, pagesize=letter)
            c.setFont("Helvetica", 12)
            
            # Position page number
            page_width, page_height = letter
            if position == 'bottom-center':
                x, y = page_width / 2 - 10, 20
            elif position == 'bottom-left':
                x, y = 50, 20
            else:  # bottom-right
                x, y = page_width - 50, 20
            
            c.drawString(x, y, str(page_num))
            c.save()
            overlay_pdf.seek(0)
            
            overlay_reader = PdfReader(overlay_pdf)
            overlay_page = overlay_reader.pages[0]
            page.merge_page(overlay_page)
            writer.add_page(page)
        
        if not output_path:
            output_path = pdf_path.rsplit('.', 1)[0] + '_numbered.pdf'
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        logger.info(f"Numbered PDF saved to: {output_path}")
        return output_path
        
    except ImportError:
        logger.error("reportlab not installed. Install with: pip install reportlab")
        raise
    except Exception as e:
        logger.error(f"Error adding page numbers: {e}")
        raise


async def crop_pdf(pdf_path: str, margins: dict, output_path: str = None) -> str:
    """
    Crop PDF pages
    
    Args:
        pdf_path: Path to input PDF
        margins: Dict with 'left', 'top', 'right', 'bottom' margins in points
        output_path: Output PDF path (optional)
        
    Returns:
        Path to output PDF
    """
    try:
        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        
        for page in reader.pages:
            page.mediabox.lower_left = (
                page.mediabox.left + margins.get('left', 0),
                page.mediabox.bottom + margins.get('bottom', 0)
            )
            page.mediabox.upper_right = (
                page.mediabox.right - margins.get('right', 0),
                page.mediabox.top - margins.get('top', 0)
            )
            writer.add_page(page)
        
        if not output_path:
            output_path = pdf_path.rsplit('.', 1)[0] + '_cropped.pdf'
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        logger.info(f"Cropped PDF saved to: {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Error cropping PDF: {e}")
        raise


async def resize_pdf(pdf_path: str, page_size: tuple, output_path: str = None) -> str:
    """
    Resize PDF pages
    
    Args:
        pdf_path: Path to input PDF
        page_size: Tuple of (width, height) in points (e.g., (595, 842) for A4)
        output_path: Output PDF path (optional)
        
    Returns:
        Path to output PDF
    """
    try:
        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        
        for page in reader.pages:
            page.scale_to(page_size[0], page_size[1])
            writer.add_page(page)
        
        if not output_path:
            output_path = pdf_path.rsplit('.', 1)[0] + '_resized.pdf'
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        logger.info(f"Resized PDF saved to: {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Error resizing PDF: {e}")
        raise


async def add_header_footer(pdf_path: str, header_text: str = None, 
                           footer_text: str = None, output_path: str = None) -> str:
    """
    Add header and/or footer to all pages
    
    Args:
        pdf_path: Path to input PDF
        header_text: Text for header (optional)
        footer_text: Text for footer (optional)
        output_path: Output PDF path (optional)
        
    Returns:
        Path to output PDF
    """
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        from io import BytesIO
        
        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        
        for page_num, page in enumerate(reader.pages, 1):
            # Create header/footer overlay
            overlay_pdf = BytesIO()
            c = canvas.Canvas(overlay_pdf, pagesize=letter)
            c.setFont("Helvetica", 10)
            
            page_width, page_height = letter
            
            # Add header
            if header_text:
                c.drawString(50, page_height - 30, header_text)
            
            # Add footer
            if footer_text:
                c.drawString(50, 30, footer_text)
            
            c.save()
            overlay_pdf.seek(0)
            
            overlay_reader = PdfReader(overlay_pdf)
            overlay_page = overlay_reader.pages[0]
            page.merge_page(overlay_page)
            writer.add_page(page)
        
        if not output_path:
            output_path = pdf_path.rsplit('.', 1)[0] + '_header_footer.pdf'
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        logger.info(f"PDF with header/footer saved to: {output_path}")
        return output_path
        
    except ImportError:
        logger.error("reportlab not installed. Install with: pip install reportlab")
        raise
    except Exception as e:
        logger.error(f"Error adding header/footer: {e}")
        raise


async def convert_to_grayscale(pdf_path: str, output_path: str = None) -> str:
    """
    Convert PDF to grayscale (black and white)
    
    Args:
        pdf_path: Path to input PDF
        output_path: Output PDF path (optional)
        
    Returns:
        Path to output PDF
    """
    try:
        import fitz  # PyMuPDF
        
        doc = fitz.open(pdf_path)
        
        for page in doc:
            # Convert to grayscale
            pix = page.get_pixmap(colorspace=fitz.csGRAY)
            img = Image.frombytes("L", [pix.width, pix.height], pix.samples)
            
            # Clear page content and add grayscale image
            page.clean_contents()
            img_bytes = img.tobytes()
            
        if not output_path:
            output_path = pdf_path.rsplit('.', 1)[0] + '_grayscale.pdf'
        
        doc.save(output_path)
        doc.close()
        
        logger.info(f"Grayscale PDF saved to: {output_path}")
        return output_path
        
    except ImportError:
        logger.error("PyMuPDF not installed. Install with: pip install PyMuPDF")
        raise
    except Exception as e:
        logger.error(f"Error converting to grayscale: {e}")
        raise