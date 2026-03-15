"""
Steps 1 & 2: Extract text and images from PDFs
"""
import fitz  # PyMuPDF
import io
from PIL import Image


def extract_text_from_pdf(pdf_path):
    """
    Extract all text from a PDF file
    
    Args:
        pdf_path: Path to the PDF file
    
    Returns:
        str: Extracted text content
    """
    print(f"\n📄 Extracting text from: {pdf_path}")
    
    doc = fitz.open(pdf_path)
    text = ""
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        page_text = page.get_text()
        text += page_text
        print(f"   Page {page_num + 1}: {len(page_text)} characters")
    
    doc.close()
    
    print(f"✅ Total text extracted: {len(text)} characters\n")
    return text


def extract_images_from_pdf(pdf_path):
    """
    Extract all images from a PDF file
    
    Args:
        pdf_path: Path to the PDF file
    
    Returns:
        list: List of dictionaries containing image data
              [{'image': bytes, 'width': int, 'height': int}, ...]
    """
    print(f"\n🖼️  Extracting images from: {pdf_path}")
    
    doc = fitz.open(pdf_path)
    images = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        image_list = page.get_images(full=True)
        
        print(f"   Page {page_num + 1}: {len(image_list)} images found")
        
        for img_index, img_info in enumerate(image_list):
            xref = img_info[0]
            
            try:
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                
                # Get image dimensions
                img = Image.open(io.BytesIO(image_bytes))
                width, height = img.size
                
                images.append({
                    'image': image_bytes,
                    'width': width,
                    'height': height,
                    'ext': image_ext,
                    'page': page_num + 1
                })
                
                print(f"      Image {img_index + 1}: {width}x{height} ({image_ext})")
            
            except Exception as e:
                print(f"      ⚠️  Could not extract image {img_index + 1}: {str(e)}")
    
    doc.close()
    
    print(f"✅ Total images extracted: {len(images)}\n")
    return images