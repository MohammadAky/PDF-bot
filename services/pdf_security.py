"""
PDF Security Services
Handles encryption, decryption, permissions, etc.
"""

import os
import logging
from PyPDF2 import PdfReader, PdfWriter

logger = logging.getLogger(__name__)


async def unlock_pdf(pdf_path: str, password: str, output_path: str = None) -> str:
    """
    Remove password protection from a PDF
    
    Args:
        pdf_path: Path to password-protected PDF
        password: Password to unlock the PDF
        output_path: Output PDF path (optional)
        
    Returns:
        Path to unlocked PDF
    """
    try:
        reader = PdfReader(pdf_path)
        
        # Try to decrypt with password
        if reader.is_encrypted:
            decrypt_result = reader.decrypt(password)
            if decrypt_result == 0:
                raise ValueError("Incorrect password")
            elif decrypt_result == 1:
                logger.info("PDF decrypted with user password")
            elif decrypt_result == 2:
                logger.info("PDF decrypted with owner password")
        else:
            logger.info("PDF is not encrypted")
        
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        
        if not output_path:
            output_path = pdf_path.rsplit('.', 1)[0] + '_unlocked.pdf'
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        logger.info(f"Unlocked PDF saved to: {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Error unlocking PDF: {e}")
        raise


async def protect_pdf(pdf_path: str, password: str, output_path: str = None,
                     owner_password: str = None, permissions: int = None) -> str:
    """
    Add password protection to a PDF
    
    Args:
        pdf_path: Path to input PDF
        password: User password to protect the PDF
        output_path: Output PDF path (optional)
        owner_password: Owner password (optional)
        permissions: Permission flags (optional)
        
    Returns:
        Path to protected PDF
    """
    try:
        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        
        for page in reader.pages:
            writer.add_page(page)
        
        # Encrypt the PDF
        if owner_password:
            writer.encrypt(
                user_password=password,
                owner_password=owner_password,
                permissions_flag=permissions
            )
        else:
            writer.encrypt(password)
        
        if not output_path:
            output_path = pdf_path.rsplit('.', 1)[0] + '_protected.pdf'
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        logger.info(f"Protected PDF saved to: {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Error protecting PDF: {e}")
        raise


async def add_permissions(pdf_path: str, allow_printing: bool = True,
                         allow_copying: bool = True, allow_modification: bool = False,
                         password: str = None, output_path: str = None) -> str:
    """
    Add permission restrictions to a PDF
    
    Args:
        pdf_path: Path to input PDF
        allow_printing: Allow printing
        allow_copying: Allow copying text
        allow_modification: Allow modifications
        password: User password (optional)
        output_path: Output PDF path (optional)
        
    Returns:
        Path to output PDF
    """
    try:
        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        
        for page in reader.pages:
            writer.add_page(page)
        
        # Build permissions flag
        permissions = 0
        if allow_printing:
            permissions |= 0b000000000100  # Printing
        if allow_copying:
            permissions |= 0b000000010000  # Copy text
        if allow_modification:
            permissions |= 0b000000001000  # Modify content
        
        # Encrypt with permissions
        if password:
            writer.encrypt(user_password=password, permissions_flag=permissions)
        else:
            writer.encrypt(user_password="", permissions_flag=permissions)
        
        if not output_path:
            output_path = pdf_path.rsplit('.', 1)[0] + '_restricted.pdf'
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        logger.info(f"PDF with permissions saved to: {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Error adding permissions: {e}")
        raise


async def remove_metadata(pdf_path: str, output_path: str = None) -> str:
    """
    Remove all metadata from a PDF
    
    Args:
        pdf_path: Path to input PDF
        output_path: Output PDF path (optional)
        
    Returns:
        Path to output PDF
    """
    try:
        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        
        for page in reader.pages:
            writer.add_page(page)
        
        # Remove metadata by not copying it
        # writer.add_metadata({})  # Empty metadata
        
        if not output_path:
            output_path = pdf_path.rsplit('.', 1)[0] + '_no_metadata.pdf'
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        logger.info(f"PDF without metadata saved to: {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Error removing metadata: {e}")
        raise


async def get_pdf_info(pdf_path: str) -> dict:
    """
    Get PDF information and metadata
    
    Args:
        pdf_path: Path to PDF
        
    Returns:
        Dictionary with PDF information
    """
    try:
        reader = PdfReader(pdf_path)
        
        info = {
            'pages': len(reader.pages),
            'encrypted': reader.is_encrypted,
            'metadata': {},
            'size': os.path.getsize(pdf_path)
        }
        
        # Get metadata if available
        if reader.metadata:
            info['metadata'] = {
                'title': reader.metadata.get('/Title', ''),
                'author': reader.metadata.get('/Author', ''),
                'subject': reader.metadata.get('/Subject', ''),
                'creator': reader.metadata.get('/Creator', ''),
                'producer': reader.metadata.get('/Producer', ''),
                'creation_date': reader.metadata.get('/CreationDate', ''),
            }
        
        logger.info(f"Retrieved info for PDF: {pdf_path}")
        return info
        
    except Exception as e:
        logger.error(f"Error getting PDF info: {e}")
        raise


async def sign_pdf(pdf_path: str, signature_path: str, output_path: str = None) -> str:
    """
    Add digital signature to PDF (placeholder - requires advanced setup)
    
    Args:
        pdf_path: Path to input PDF
        signature_path: Path to signature certificate
        output_path: Output PDF path (optional)
        
    Returns:
        Path to signed PDF
    """
    try:
        # This is a placeholder - digital signatures require:
        # 1. Digital certificate
        # 2. Private key
        # 3. Advanced PDF signing library like pyHanko or endesive
        
        raise NotImplementedError(
            "Digital signatures require advanced setup. "
            "Please install pyHanko: pip install pyHanko"
        )
        
    except Exception as e:
        logger.error(f"Error signing PDF: {e}")
        raise


async def redact_pdf(pdf_path: str, areas: list, output_path: str = None) -> str:
    """
    Redact (permanently remove) content from PDF areas
    
    Args:
        pdf_path: Path to input PDF
        areas: List of areas to redact (page_num, x1, y1, x2, y2)
        output_path: Output PDF path (optional)
        
    Returns:
        Path to redacted PDF
    """
    try:
        import fitz  # PyMuPDF
        
        doc = fitz.open(pdf_path)
        
        for area in areas:
            page_num, x1, y1, x2, y2 = area
            page = doc[page_num]
            
            # Create redaction annotation
            redact_area = fitz.Rect(x1, y1, x2, y2)
            page.add_redact_annot(redact_area, fill=(0, 0, 0))
        
        # Apply redactions
        doc.apply_redactions()
        
        if not output_path:
            output_path = pdf_path.rsplit('.', 1)[0] + '_redacted.pdf'
        
        doc.save(output_path)
        doc.close()
        
        logger.info(f"Redacted PDF saved to: {output_path}")
        return output_path
        
    except ImportError:
        logger.error("PyMuPDF not installed. Install with: pip install PyMuPDF")
        raise
    except Exception as e:
        logger.error(f"Error redacting PDF: {e}")
        raise


async def compare_pdfs(pdf_path1: str, pdf_path2: str, output_path: str = None) -> dict:
    """
    Compare two PDF files
    
    Args:
        pdf_path1: Path to first PDF
        pdf_path2: Path to second PDF
        output_path: Output comparison report path (optional)
        
    Returns:
        Dictionary with comparison results
    """
    try:
        reader1 = PdfReader(pdf_path1)
        reader2 = PdfReader(pdf_path2)
        
        comparison = {
            'pages_match': len(reader1.pages) == len(reader2.pages),
            'page_count_1': len(reader1.pages),
            'page_count_2': len(reader2.pages),
            'size_1': os.path.getsize(pdf_path1),
            'size_2': os.path.getsize(pdf_path2),
            'differences': []
        }
        
        # Compare page by page
        for i in range(min(len(reader1.pages), len(reader2.pages))):
            page1 = reader1.pages[i]
            page2 = reader2.pages[i]
            
            # Extract text for comparison
            text1 = page1.extract_text()
            text2 = page2.extract_text()
            
            if text1 != text2:
                comparison['differences'].append({
                    'page': i + 1,
                    'type': 'text_difference'
                })
        
        logger.info(f"Compared PDFs: {len(comparison['differences'])} differences found")
        return comparison
        
    except Exception as e:
        logger.error(f"Error comparing PDFs: {e}")
        raise