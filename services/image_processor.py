"""
Image Processing Services
"""

import os
import logging
from typing import List
from PIL import Image

logger = logging.getLogger(__name__)


async def images_to_pdf(image_paths: List[str], output_path: str = None) -> str:
    """
    Convert multiple images to a single PDF
    
    Args:
        image_paths: List of paths to image files
        output_path: Output PDF path (optional)
        
    Returns:
        Path to output PDF
    """
    try:
        if not image_paths:
            raise ValueError("No images provided")
        
        # Open all images and convert to RGB
        images = []
        for img_path in image_paths:
            try:
                img = Image.open(img_path)
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                images.append(img)
                logger.info(f"Loaded image: {img_path}")
            except Exception as e:
                logger.error(f"Error loading image {img_path}: {e}")
                continue
        
        if not images:
            raise ValueError("No valid images found")
        
        # Create output path if not provided
        if not output_path:
            output_dir = os.path.dirname(image_paths[0])
            output_path = os.path.join(output_dir, 'images_combined.pdf')
        
        # Save all images as a single PDF
        if len(images) == 1:
            images[0].save(output_path, 'PDF', resolution=100.0)
        else:
            images[0].save(
                output_path,
                'PDF',
                resolution=100.0,
                save_all=True,
                append_images=images[1:]
            )
        
        logger.info(f"Created PDF from {len(images)} images: {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Error converting images to PDF: {e}")
        raise


async def pdf_to_images(pdf_path: str, output_dir: str = None, format: str = 'jpg') -> List[str]:
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
        
    except Exception as e:
        logger.error(f"Error converting PDF to images: {e}")
        raise


async def resize_image(image_path: str, max_width: int = 1920, max_height: int = 1920) -> str:
    """
    Resize image maintaining aspect ratio
    
    Args:
        image_path: Path to image
        max_width: Maximum width
        max_height: Maximum height
        
    Returns:
        Path to resized image (same as input)
    """
    try:
        img = Image.open(image_path)
        
        # Calculate new size maintaining aspect ratio
        img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
        
        # Save back to same path
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        
        img.save(image_path, quality=95)
        logger.info(f"Resized image: {image_path}")
        
        return image_path
        
    except Exception as e:
        logger.error(f"Error resizing image: {e}")
        raise


async def compress_image(image_path: str, quality: int = 85) -> str:
    """
    Compress image
    
    Args:
        image_path: Path to image
        quality: JPEG quality (1-100)
        
    Returns:
        Path to compressed image
    """
    try:
        img = Image.open(image_path)
        
        output_path = image_path.rsplit('.', 1)[0] + '_compressed.jpg'
        
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        
        img.save(output_path, 'JPEG', quality=quality, optimize=True)
        logger.info(f"Compressed image: {output_path}")
        
        return output_path
        
    except Exception as e:
        logger.error(f"Error compressing image: {e}")
        raise


async def convert_image_format(image_path: str, target_format: str) -> str:
    """
    Convert image to different format
    
    Args:
        image_path: Path to input image
        target_format: Target format ('jpg', 'png', 'webp', etc.)
        
    Returns:
        Path to converted image
    """
    try:
        img = Image.open(image_path)
        
        output_path = image_path.rsplit('.', 1)[0] + f'.{target_format.lower()}'
        
        if target_format.lower() in ['jpg', 'jpeg']:
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            img.save(output_path, 'JPEG', quality=95)
        elif target_format.lower() == 'png':
            img.save(output_path, 'PNG')
        elif target_format.lower() == 'webp':
            img.save(output_path, 'WEBP', quality=95)
        else:
            img.save(output_path)
        
        logger.info(f"Converted image to {target_format.upper()}: {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Error converting image format: {e}")
        raise


async def rotate_image(image_path: str, angle: int) -> str:
    """
    Rotate image
    
    Args:
        image_path: Path to image
        angle: Rotation angle (90, 180, 270)
        
    Returns:
        Path to rotated image
    """
    try:
        img = Image.open(image_path)
        
        # Rotate image
        rotated = img.rotate(-angle, expand=True)
        
        output_path = image_path.rsplit('.', 1)[0] + '_rotated.' + image_path.rsplit('.', 1)[1]
        
        rotated.save(output_path)
        logger.info(f"Rotated image {angle}°: {output_path}")
        
        return output_path
        
    except Exception as e:
        logger.error(f"Error rotating image: {e}")
        raise