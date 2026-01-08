"""
PDF Organization Services
Handles merging, splitting, extracting, and removing pages
"""

import os
import logging
from typing import List, Tuple, Union
from PyPDF2 import PdfReader, PdfWriter, PdfMerger

# Optional import for better performance
try:
    import fitz  # PyMuPDF
    HAS_FITZ = True
except ImportError:
    HAS_FITZ = False

logger = logging.getLogger(__name__)


class PDFOrganizer:
    """PDF organization operations"""
    
    @staticmethod
    async def merge_pdfs(pdf_paths: List[str], output_path: str = None) -> str:
        """
        Merge multiple PDF files into one
        
        Args:
            pdf_paths: List of PDF file paths
            output_path: Output file path (optional)
            
        Returns:
            Path to merged PDF
        """
        try:
            if not pdf_paths:
                raise ValueError("No PDF files provided")
            
            if len(pdf_paths) < 2:
                raise ValueError("At least 2 PDF files required for merging")
            
            # Create output path if not provided
            if not output_path:
                output_dir = os.path.dirname(pdf_paths[0])
                output_path = os.path.join(output_dir, 'merged_output.pdf')
            
            merger = PdfMerger()
            
            # Add each PDF to the merger
            for pdf_path in pdf_paths:
                if not os.path.exists(pdf_path):
                    logger.warning(f"PDF file not found: {pdf_path}")
                    continue
                    
                if not pdf_path.lower().endswith('.pdf'):
                    logger.warning(f"Not a PDF file: {pdf_path}")
                    continue
                
                try:
                    merger.append(pdf_path)
                    logger.info(f"Added PDF to merger: {pdf_path}")
                except Exception as e:
                    logger.error(f"Failed to add {pdf_path}: {e}")
                    continue
            
            # Write the merged PDF
            merger.write(output_path)
            merger.close()
            
            logger.info(f"PDFs merged successfully: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error merging PDFs: {e}")
            raise
    
    @staticmethod
    async def split_pdf(pdf_path: str, split_mode: str) -> List[str]:
        """
        Split a PDF file
        
        Args:
            pdf_path: Path to input PDF
            split_mode: Split mode:
                - "every N" - Split every N pages (e.g., "every 2")
                - "1-5,6-10" - Split by page ranges
                - "1,3,5" - Extract specific pages
                
        Returns:
            List of output PDF paths
        """
        try:
            reader = PdfReader(pdf_path)
            total_pages = len(reader.pages)
            output_paths = []
            
            # Parse split mode
            if split_mode.startswith("every "):
                # Split every N pages
                n = int(split_mode.split()[1])
                page_ranges = [(i, min(i + n, total_pages)) 
                             for i in range(0, total_pages, n)]
                
            elif "," in split_mode or "-" in split_mode:
                # Parse page ranges and individual pages
                page_ranges = PDFOrganizer._parse_page_specification(
                    split_mode, total_pages
                )
            else:
                raise ValueError(f"Invalid split mode: {split_mode}")
            
            # Create split PDFs
            for i, page_range in enumerate(page_ranges):
                writer = PdfWriter()
                
                if isinstance(page_range, tuple):
                    start, end = page_range
                    for page_num in range(start, end):
                        if 0 <= page_num < total_pages:
                            writer.add_page(reader.pages[page_num])
                else:
                    # Single page
                    if 0 <= page_range < total_pages:
                        writer.add_page(reader.pages[page_range])
                
                output_path = pdf_path.rsplit('.', 1)[0] + f'_part_{i+1}.pdf'
                
                with open(output_path, 'wb') as output_file:
                    writer.write(output_file)
                
                output_paths.append(output_path)
                logger.info(f"Created split PDF: {output_path}")
            
            return output_paths
            
        except Exception as e:
            logger.error(f"Error splitting PDF: {e}")
            raise
    
    @staticmethod
    async def extract_pages(pdf_path: str, page_spec: str, output_path: str = None) -> str:
        """
        Extract specific pages from a PDF
        
        Args:
            pdf_path: Path to input PDF
            page_spec: Page specification (e.g., "1,3,5" or "1-5,8,10-15")
            output_path: Output file path (optional)
            
        Returns:
            Path to output PDF
        """
        try:
            reader = PdfReader(pdf_path)
            writer = PdfWriter()
            total_pages = len(reader.pages)
            
            # Parse page specification
            page_numbers = PDFOrganizer._parse_page_specification(
                page_spec, total_pages, flatten=True
            )
            
            # Add pages
            for page_num in sorted(set(page_numbers)):
                if 0 <= page_num < total_pages:
                    writer.add_page(reader.pages[page_num])
            
            # Create output path
            if not output_path:
                output_path = pdf_path.rsplit('.', 1)[0] + '_extracted.pdf'
            
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            logger.info(f"Extracted {len(page_numbers)} pages to: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error extracting pages: {e}")
            raise
    
    @staticmethod
    async def remove_pages(pdf_path: str, page_spec: str, output_path: str = None) -> str:
        """
        Remove specific pages from a PDF
        
        Args:
            pdf_path: Path to input PDF
            page_spec: Page specification (e.g., "1,3,5" or "1-5,8,10-15")
            output_path: Output file path (optional)
            
        Returns:
            Path to output PDF
        """
        try:
            reader = PdfReader(pdf_path)
            writer = PdfWriter()
            total_pages = len(reader.pages)
            
            # Parse page specification
            pages_to_remove = set(PDFOrganizer._parse_page_specification(
                page_spec, total_pages, flatten=True
            ))
            
            # Add pages that are NOT in the remove list
            for page_num in range(total_pages):
                if page_num not in pages_to_remove:
                    writer.add_page(reader.pages[page_num])
            
            # Create output path
            if not output_path:
                output_path = pdf_path.rsplit('.', 1)[0] + '_removed.pdf'
            
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            logger.info(f"Removed {len(pages_to_remove)} pages, saved to: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error removing pages: {e}")
            raise
    
    @staticmethod
    async def reorder_pages(pdf_path: str, page_order: str, output_path: str = None) -> str:
        """
        Reorder pages in a PDF
        
        Args:
            pdf_path: Path to input PDF
            page_order: New page order (e.g., "3,1,2" or "5-1,6-10")
            output_path: Output file path (optional)
            
        Returns:
            Path to output PDF
        """
        try:
            reader = PdfReader(pdf_path)
            writer = PdfWriter()
            total_pages = len(reader.pages)
            
            # Parse page order
            page_sequence = PDFOrganizer._parse_page_specification(
                page_order, total_pages, flatten=True
            )
            
            # Add pages in specified order
            for page_num in page_sequence:
                if 0 <= page_num < total_pages:
                    writer.add_page(reader.pages[page_num])
            
            # Create output path
            if not output_path:
                output_path = pdf_path.rsplit('.', 1)[0] + '_reordered.pdf'
            
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            logger.info(f"Reordered pages, saved to: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error reordering pages: {e}")
            raise
    
    @staticmethod
    async def extract_images(pdf_path: str, output_dir: str = None) -> List[str]:
        """
        Extract all images from a PDF
        
        Args:
            pdf_path: Path to input PDF
            output_dir: Output directory (optional)
            
        Returns:
            List of extracted image paths
        """
        try:
            if not HAS_FITZ:
                raise ImportError("PyMuPDF (fitz) is required for image extraction. Install with: pip install PyMuPDF")
            
            if not output_dir:
                output_dir = os.path.dirname(pdf_path)
            
            doc = fitz.open(pdf_path)
            image_paths = []
            image_count = 0
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                image_list = page.get_images()
                
                for img_index, img in enumerate(image_list):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    
                    image_count += 1
                    image_filename = f"extracted_image_{image_count}.{image_ext}"
                    image_path = os.path.join(output_dir, image_filename)
                    
                    with open(image_path, "wb") as img_file:
                        img_file.write(image_bytes)
                    
                    image_paths.append(image_path)
                    logger.info(f"Extracted image: {image_path}")
            
            doc.close()
            logger.info(f"Extracted {len(image_paths)} images from PDF")
            return image_paths
            
        except Exception as e:
            logger.error(f"Error extracting images: {e}")
            raise
    
    @staticmethod
    async def extract_text(pdf_path: str, output_path: str = None) -> str:
        """
        Extract all text from a PDF
        
        Args:
            pdf_path: Path to input PDF
            output_path: Output text file path (optional)
            
        Returns:
            Path to output text file or extracted text
        """
        try:
            if HAS_FITZ:
                # Use PyMuPDF if available (better text extraction)
                doc = fitz.open(pdf_path)
                text_content = []
                
                for page_num in range(len(doc)):
                    page = doc[page_num]
                    text = page.get_text()
                    text_content.append(f"--- Page {page_num + 1} ---\n{text}\n")
                
                doc.close()
            else:
                # Fallback to PyPDF2
                reader = PdfReader(pdf_path)
                text_content = []
                
                for page_num, page in enumerate(reader.pages):
                    text = page.extract_text()
                    text_content.append(f"--- Page {page_num + 1} ---\n{text}\n")
            
            full_text = "\n".join(text_content)
            
            if output_path:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(full_text)
                logger.info(f"Extracted text saved to: {output_path}")
                return output_path
            
            return full_text
            
        except Exception as e:
            logger.error(f"Error extracting text: {e}")
            raise
    
    @staticmethod
    def _parse_page_specification(
        spec: str, 
        total_pages: int, 
        flatten: bool = False
    ) -> Union[List[int], List[Tuple[int, int]]]:
        """
        Parse page specification string
        
        Args:
            spec: Page specification (e.g., "1,3,5" or "1-5,8,10-15")
            total_pages: Total number of pages
            flatten: If True, return flat list of page numbers
            
        Returns:
            List of page numbers (0-indexed) or page ranges
        """
        pages = []
        parts = spec.replace(" ", "").split(",")
        
        for part in parts:
            if "-" in part:
                # Page range
                start, end = part.split("-")
                start_page = int(start) - 1  # Convert to 0-indexed
                end_page = int(end)  # Keep as 1-indexed for range
                
                if flatten:
                    pages.extend(range(start_page, min(end_page, total_pages)))
                else:
                    pages.append((start_page, min(end_page, total_pages)))
            else:
                # Single page
                page_num = int(part) - 1  # Convert to 0-indexed
                if flatten:
                    if 0 <= page_num < total_pages:
                        pages.append(page_num)
                else:
                    pages.append(page_num)
        
        return pages


# Convenience functions
async def merge_pdfs(pdf_paths: List[str], output_path: str = None) -> str:
    """Merge multiple PDFs"""
    return await PDFOrganizer.merge_pdfs(pdf_paths, output_path)


async def split_pdf(pdf_path: str, split_mode: str) -> List[str]:
    """Split a PDF"""
    return await PDFOrganizer.split_pdf(pdf_path, split_mode)


async def extract_pages(pdf_path: str, page_spec: str, output_path: str = None) -> str:
    """Extract pages from PDF"""
    return await PDFOrganizer.extract_pages(pdf_path, page_spec, output_path)


async def remove_pages(pdf_path: str, page_spec: str, output_path: str = None) -> str:
    """Remove pages from PDF"""
    return await PDFOrganizer.remove_pages(pdf_path, page_spec, output_path)


async def extract_images(pdf_path: str, output_dir: str = None) -> List[str]:
    """Extract images from PDF"""
    return await PDFOrganizer.extract_images(pdf_path, output_dir)


async def extract_text(pdf_path: str, output_path: str = None) -> str:
    """Extract text from PDF"""
    return await PDFOrganizer.extract_text(pdf_path, output_path)