"""
PDF Conversion Services
Handles conversion between PDF and other formats
"""

import os
import logging
from typing import Optional
from PIL import Image
from fpdf import FPDF

logger = logging.getLogger(__name__)


async def convert_image_to_pdf(image_path: str, output_path: str = None) -> str:
    """
    Convert an image to PDF format
    
    Args:
        image_path: Path to input image
        output_path: Output PDF path (optional)
        
    Returns:
        Path to output PDF
    """
    try:
        # Open the image
        image = Image.open(image_path)
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Create output path if not provided
        if not output_path:
            output_path = image_path.rsplit('.', 1)[0] + '_converted.pdf'
        
        # Save as PDF
        image.save(output_path, 'PDF', resolution=100.0)
        
        logger.info(f"Image converted successfully: {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Error converting image to PDF: {e}")
        raise


async def convert_document_to_pdf(doc_path: str, output_path: str = None) -> str:
    """
    Convert a document (DOCX, TXT, etc.) to PDF format
    
    Args:
        doc_path: Path to input document
        output_path: Output PDF path (optional)
        
    Returns:
        Path to output PDF
    """
    try:
        file_ext = doc_path.rsplit('.', 1)[-1].lower()
        
        if not output_path:
            output_path = doc_path.rsplit('.', 1)[0] + '_converted.pdf'
        
        if file_ext == 'docx':
            # Convert DOCX to PDF
            try:
                from docx2pdf import convert as docx_convert
                docx_convert(doc_path, output_path)
            except ImportError:
                logger.warning("docx2pdf not available, trying alternative method")
                # Fallback: try using LibreOffice if available
                import subprocess
                try:
                    subprocess.run([
                        'libreoffice', '--headless', '--convert-to', 'pdf',
                        '--outdir', os.path.dirname(output_path), doc_path
                    ], check=True, capture_output=True)
                except FileNotFoundError:
                    raise Exception("Neither docx2pdf nor LibreOffice available for DOCX conversion")
        
        elif file_ext == 'txt':
            # Convert TXT to PDF using FPDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            
            with open(doc_path, 'r', encoding='utf-8', errors='ignore') as file:
                for line in file:
                    try:
                        pdf.multi_cell(0, 10, txt=line.strip())
                    except:
                        # Skip lines with encoding issues
                        continue
            
            pdf.output(output_path)
        
        elif file_ext == 'pdf':
            # Already PDF, just return it
            return doc_path
        
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")
        
        logger.info(f"Document converted successfully: {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Error converting document to PDF: {e}")
        raise


async def pdf_to_text(pdf_path: str, output_path: str = None) -> str:
    """
    Extract text from PDF to TXT file
    
    Args:
        pdf_path: Path to input PDF
        output_path: Output text file path (optional)
        
    Returns:
        Path to output text file
    """
    try:
        import fitz  # PyMuPDF
        
        doc = fitz.open(pdf_path)
        text_content = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            text_content.append(f"--- Page {page_num + 1} ---\n{text}\n")
        
        doc.close()
        
        full_text = "\n".join(text_content)
        
        if not output_path:
            output_path = pdf_path.rsplit('.', 1)[0] + '.txt'
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(full_text)
        
        logger.info(f"Text extracted to: {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {e}")
        raise


async def pdf_to_images(pdf_path: str, output_dir: str = None, format: str = 'jpg') -> list:
    """
    Convert PDF pages to images
    
    Args:
        pdf_path: Path to input PDF
        output_dir: Output directory (optional)
        format: Image format ('jpg' or 'png')
        
    Returns:
        List of image paths
    """
    try:
        from pdf2image import convert_from_path
        
        if not output_dir:
            output_dir = os.path.dirname(pdf_path)
        
        # Convert PDF to images
        images = convert_from_path(pdf_path, dpi=300)
        image_paths = []
        
        for i, image in enumerate(images):
            output_path = os.path.join(
                output_dir,
                f"page_{i+1}.{format}"
            )
            
            if format.lower() == 'jpg':
                image = image.convert('RGB')
                image.save(output_path, 'JPEG', quality=95)
            else:
                image.save(output_path, 'PNG')
            
            image_paths.append(output_path)
            logger.info(f"Converted page {i+1} to image: {output_path}")
        
        logger.info(f"Converted {len(image_paths)} pages to {format.upper()}")
        return image_paths
        
    except ImportError:
        logger.error("pdf2image not installed. Install with: pip install pdf2image")
        raise
    except Exception as e:
        logger.error(f"Error converting PDF to images: {e}")
        raise


async def word_to_pdf(doc_path: str, output_path: str = None) -> str:
    """
    Convert Word document to PDF
    
    Args:
        doc_path: Path to Word document
        output_path: Output PDF path (optional)
        
    Returns:
        Path to output PDF
    """
    return await convert_document_to_pdf(doc_path, output_path)


async def excel_to_pdf(excel_path: str, output_path: str = None) -> str:
    """
    Convert Excel to PDF
    
    Args:
        excel_path: Path to Excel file
        output_path: Output PDF path (optional)
        
    Returns:
        Path to output PDF
    """
    try:
        import subprocess
        
        if not output_path:
            output_path = excel_path.rsplit('.', 1)[0] + '.pdf'
        
        # Try using LibreOffice
        try:
            subprocess.run([
                'libreoffice', '--headless', '--convert-to', 'pdf',
                '--outdir', os.path.dirname(output_path), excel_path
            ], check=True, capture_output=True)
            
            logger.info(f"Excel converted successfully: {output_path}")
            return output_path
        except FileNotFoundError:
            raise Exception("LibreOffice not available for Excel conversion")
        
    except Exception as e:
        logger.error(f"Error converting Excel to PDF: {e}")
        raise


async def powerpoint_to_pdf(ppt_path: str, output_path: str = None) -> str:
    """
    Convert PowerPoint to PDF
    
    Args:
        ppt_path: Path to PowerPoint file
        output_path: Output PDF path (optional)
        
    Returns:
        Path to output PDF
    """
    try:
        import subprocess
        
        if not output_path:
            output_path = ppt_path.rsplit('.', 1)[0] + '.pdf'
        
        # Try using LibreOffice
        try:
            subprocess.run([
                'libreoffice', '--headless', '--convert-to', 'pdf',
                '--outdir', os.path.dirname(output_path), ppt_path
            ], check=True, capture_output=True)
            
            logger.info(f"PowerPoint converted successfully: {output_path}")
            return output_path
        except FileNotFoundError:
            raise Exception("LibreOffice not available for PowerPoint conversion")
        
    except Exception as e:
        logger.error(f"Error converting PowerPoint to PDF: {e}")
        raise


async def html_to_pdf(html_path: str, output_path: str = None) -> str:
    """
    Convert HTML to PDF
    
    Args:
        html_path: Path to HTML file
        output_path: Output PDF path (optional)
        
    Returns:
        Path to output PDF
    """
    try:
        import pdfkit
        
        if not output_path:
            output_path = html_path.rsplit('.', 1)[0] + '.pdf'
        
        pdfkit.from_file(html_path, output_path)
        
        logger.info(f"HTML converted successfully: {output_path}")
        return output_path
        
    except ImportError:
        logger.error("pdfkit not installed. Install with: pip install pdfkit")
        raise
    except Exception as e:
        logger.error(f"Error converting HTML to PDF: {e}")
        raise


async def pdf_to_word(pdf_path: str, output_path: str = None) -> str:
    """
    Convert PDF to Word document
    
    Args:
        pdf_path: Path to input PDF
        output_path: Output Word file path (optional)
        
    Returns:
        Path to output Word file
    """
    try:
        from pdf2docx import Converter
        
        if not output_path:
            output_path = pdf_path.rsplit('.', 1)[0] + '.docx'
        
        cv = Converter(pdf_path)
        cv.convert(output_path)
        cv.close()
        
        logger.info(f"PDF converted to Word: {output_path}")
        return output_path
        
    except ImportError:
        logger.error("pdf2docx not installed. Install with: pip install pdf2docx")
        raise
    except Exception as e:
        logger.error(f"Error converting PDF to Word: {e}")
        raise


async def pdf_to_excel(pdf_path: str, output_path: str = None) -> str:
    """
    Convert PDF to Excel (extract tables)
    
    Args:
        pdf_path: Path to input PDF
        output_path: Output Excel file path (optional)
        
    Returns:
        Path to output Excel file
    """
    try:
        import pdfplumber
        import pandas as pd
        
        if not output_path:
            output_path = pdf_path.rsplit('.', 1)[0] + '.xlsx'
        
        all_tables = []
        
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                all_tables.extend(tables)
        
        if not all_tables:
            raise ValueError("No tables found in PDF")
        
        # Write to Excel
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            for i, table in enumerate(all_tables):
                df = pd.DataFrame(table[1:], columns=table[0])
                df.to_excel(writer, sheet_name=f'Table_{i+1}', index=False)
        
        logger.info(f"PDF converted to Excel: {output_path}")
        return output_path
        
    except ImportError:
        logger.error("Required libraries not installed. Install with: pip install pdfplumber pandas openpyxl")
        raise
    except Exception as e:
        logger.error(f"Error converting PDF to Excel: {e}")
        raise