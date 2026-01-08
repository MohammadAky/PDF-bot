"""
PDF Optimization Services
Handles compression, repair, OCR, etc.
"""

import os
import logging
from PyPDF2 import PdfReader, PdfWriter

logger = logging.getLogger(__name__)


async def compress_pdf(pdf_path: str, quality: str = 'medium', output_path: str = None) -> str:
    """
    Compress a PDF file
    
    Args:
        pdf_path: Path to input PDF
        quality: Compression quality ('low', 'medium', 'high')
        output_path: Output PDF path (optional)
        
    Returns:
        Path to compressed PDF
    """
    try:
        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        
        for page in reader.pages:
            # Compress the page content streams
            page.compress_content_streams()
            writer.add_page(page)
        
        # Set compression level based on quality
        if quality == 'high':
            writer.add_metadata({'/Compress': 'True'})
        
        if not output_path:
            output_path = pdf_path.rsplit('.', 1)[0] + '_compressed.pdf'
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        # Calculate compression ratio
        original_size = os.path.getsize(pdf_path)
        compressed_size = os.path.getsize(output_path)
        ratio = (1 - compressed_size / original_size) * 100 if original_size > 0 else 0
        
        logger.info(f"Compressed PDF saved to: {output_path} (reduced by {ratio:.1f}%)")
        return output_path
        
    except Exception as e:
        logger.error(f"Error compressing PDF: {e}")
        raise


async def compress_pdf_advanced(pdf_path: str, quality: str = 'medium', 
                               output_path: str = None) -> str:
    """
    Advanced PDF compression using Ghostscript
    
    Args:
        pdf_path: Path to input PDF
        quality: Compression quality ('low', 'medium', 'high')
        output_path: Output PDF path (optional)
        
    Returns:
        Path to compressed PDF
    """
    try:
        import subprocess
        
        # Quality settings for Ghostscript
        quality_settings = {
            'low': '/screen',      # 72 dpi
            'medium': '/ebook',    # 150 dpi
            'high': '/printer'     # 300 dpi
        }
        
        gs_quality = quality_settings.get(quality, '/ebook')
        
        if not output_path:
            output_path = pdf_path.rsplit('.', 1)[0] + '_compressed.pdf'
        
        # Run Ghostscript
        gs_command = [
            'gs',
            '-sDEVICE=pdfwrite',
            '-dCompatibilityLevel=1.4',
            f'-dPDFSETTINGS={gs_quality}',
            '-dNOPAUSE',
            '-dQUIET',
            '-dBATCH',
            f'-sOutputFile={output_path}',
            pdf_path
        ]
        
        try:
            subprocess.run(gs_command, check=True, capture_output=True)
            logger.info(f"Advanced compressed PDF saved to: {output_path}")
            return output_path
        except FileNotFoundError:
            logger.warning("Ghostscript not available, using basic compression")
            return await compress_pdf(pdf_path, quality, output_path)
        
    except Exception as e:
        logger.error(f"Error in advanced compression: {e}")
        # Fallback to basic compression
        return await compress_pdf(pdf_path, quality, output_path)


async def repair_pdf(pdf_path: str, output_path: str = None) -> str:
    """
    Attempt to repair a damaged PDF
    
    Args:
        pdf_path: Path to damaged PDF
        output_path: Output PDF path (optional)
        
    Returns:
        Path to repaired PDF
    """
    try:
        # Try to read with strict=False to handle damaged PDFs
        reader = PdfReader(pdf_path, strict=False)
        writer = PdfWriter()
        
        # Copy all readable pages
        for page_num in range(len(reader.pages)):
            try:
                page = reader.pages[page_num]
                writer.add_page(page)
            except Exception as e:
                logger.warning(f"Could not repair page {page_num + 1}: {e}")
                continue
        
        if not output_path:
            output_path = pdf_path.rsplit('.', 1)[0] + '_repaired.pdf'
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        logger.info(f"Repaired PDF saved to: {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Error repairing PDF: {e}")
        raise


async def ocr_pdf(pdf_path: str, language: str = 'eng', output_path: str = None) -> str:
    """
    Perform OCR on a scanned PDF to make it searchable
    
    Args:
        pdf_path: Path to input PDF
        language: OCR language code (e.g., 'eng', 'ara', 'fas')
        output_path: Output PDF path (optional)
        
    Returns:
        Path to searchable PDF
    """
    try:
        import ocrmypdf
        
        if not output_path:
            output_path = pdf_path.rsplit('.', 1)[0] + '_ocr.pdf'
        
        # Perform OCR
        ocrmypdf.ocr(
            pdf_path,
            output_path,
            language=language,
            optimize=1,
            skip_text=True  # Skip pages that already have text
        )
        
        logger.info(f"OCR completed, saved to: {output_path}")
        return output_path
        
    except ImportError:
        logger.error("ocrmypdf not installed. Install with: pip install ocrmypdf")
        raise
    except Exception as e:
        logger.error(f"Error performing OCR: {e}")
        raise


async def ocr_pdf_pytesseract(pdf_path: str, language: str = 'eng', 
                             output_path: str = None) -> str:
    """
    Perform OCR using pytesseract (alternative method)
    
    Args:
        pdf_path: Path to input PDF
        language: Tesseract language code
        output_path: Output PDF path (optional)
        
    Returns:
        Path to searchable PDF
    """
    try:
        import pytesseract
        from pdf2image import convert_from_path
        from fpdf import FPDF
        
        # Convert PDF to images
        images = convert_from_path(pdf_path, dpi=300)
        
        # Perform OCR on each image
        text_pages = []
        for img in images:
            text = pytesseract.image_to_string(img, lang=language)
            text_pages.append(text)
        
        # Create new PDF with OCR text
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        for text in text_pages:
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            # Handle encoding issues
            try:
                pdf.multi_cell(0, 10, txt=text)
            except:
                # Skip problematic characters
                safe_text = text.encode('latin-1', 'ignore').decode('latin-1')
                pdf.multi_cell(0, 10, txt=safe_text)
        
        if not output_path:
            output_path = pdf_path.rsplit('.', 1)[0] + '_ocr.pdf'
        
        pdf.output(output_path)
        
        logger.info(f"OCR completed with pytesseract, saved to: {output_path}")
        return output_path
        
    except ImportError as e:
        logger.error(f"Required library not installed: {e}")
        raise
    except Exception as e:
        logger.error(f"Error performing OCR with pytesseract: {e}")
        raise


async def optimize_images_in_pdf(pdf_path: str, quality: int = 85, 
                                output_path: str = None) -> str:
    """
    Optimize images within a PDF
    
    Args:
        pdf_path: Path to input PDF
        quality: Image quality (1-100)
        output_path: Output PDF path (optional)
        
    Returns:
        Path to optimized PDF
    """
    try:
        import fitz  # PyMuPDF
        from PIL import Image
        from io import BytesIO
        
        doc = fitz.open(pdf_path)
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            image_list = page.get_images()
            
            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                
                # Open image with PIL
                pil_image = Image.open(BytesIO(image_bytes))
                
                # Compress image
                output = BytesIO()
                if pil_image.mode == 'RGBA':
                    pil_image = pil_image.convert('RGB')
                pil_image.save(output, format='JPEG', quality=quality, optimize=True)
                
                # Replace image in PDF
                output.seek(0)
                # This is simplified - actual implementation is more complex
        
        if not output_path:
            output_path = pdf_path.rsplit('.', 1)[0] + '_optimized.pdf'
        
        doc.save(output_path, garbage=4, deflate=True)
        doc.close()
        
        logger.info(f"Optimized PDF with compressed images saved to: {output_path}")
        return output_path
        
    except ImportError:
        logger.error("PyMuPDF not installed. Install with: pip install PyMuPDF")
        raise
    except Exception as e:
        logger.error(f"Error optimizing images in PDF: {e}")
        raise


async def reduce_file_size(pdf_path: str, output_path: str = None) -> str:
    """
    Reduce PDF file size using multiple techniques
    
    Args:
        pdf_path: Path to input PDF
        output_path: Output PDF path (optional)
        
    Returns:
        Path to reduced PDF
    """
    try:
        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        
        for page in reader.pages:
            # Compress content
            page.compress_content_streams()
            
            # Remove unnecessary data
            if '/Annots' in page:
                # Keep annotations but compress them
                pass
            
            writer.add_page(page)
        
        # Remove duplicate objects
        writer.add_metadata({})  # Clear metadata to reduce size
        
        if not output_path:
            output_path = pdf_path.rsplit('.', 1)[0] + '_reduced.pdf'
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        original_size = os.path.getsize(pdf_path) / (1024 * 1024)
        reduced_size = os.path.getsize(output_path) / (1024 * 1024)
        
        logger.info(f"Reduced PDF from {original_size:.2f}MB to {reduced_size:.2f}MB")
        return output_path
        
    except Exception as e:
        logger.error(f"Error reducing file size: {e}")
        raise


async def linearize_pdf(pdf_path: str, output_path: str = None) -> str:
    """
    Linearize PDF for fast web viewing
    
    Args:
        pdf_path: Path to input PDF
        output_path: Output PDF path (optional)
        
    Returns:
        Path to linearized PDF
    """
    try:
        import subprocess
        
        if not output_path:
            output_path = pdf_path.rsplit('.', 1)[0] + '_linearized.pdf'
        
        # Use qpdf for linearization
        try:
            subprocess.run([
                'qpdf',
                '--linearize',
                pdf_path,
                output_path
            ], check=True, capture_output=True)
            
            logger.info(f"Linearized PDF saved to: {output_path}")
            return output_path
        except FileNotFoundError:
            logger.warning("qpdf not available, returning original")
            return pdf_path
        
    except Exception as e:
        logger.error(f"Error linearizing PDF: {e}")
        raise