import fitz
import io
from PIL import Image

fitz.TOOLS.mupdf_display_errors(False)


def extract_pdf_text(file):
    """Extract all text from a PDF file."""
    text = ""
    file.seek(0)
    doc = fitz.open(stream=file.read(), filetype="pdf")
    
    for page in doc:
        text += page.get_text()
    
    doc.close()
    return text


def extract_images_from_pdf(file):
    """Extract images from PDF with metadata."""
    images = []
    file.seek(0)
    doc = fitz.open(stream=file.read(), filetype="pdf")
    
    for page_num, page in enumerate(doc):
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            try:
                base = doc.extract_image(xref)
                img_bytes = base["image"]
                width = base["width"]
                height = base["height"]
                
                # Filter out small images (logos, icons)
                if width < 200 or height < 200:
                    continue
                
                # Store image with metadata
                images.append({
                    'image': io.BytesIO(img_bytes),
                    'width': width,
                    'height': height,
                    'page': page_num + 1,
                    'index': img_index
                })
            except Exception as e:
                print(f"Error extracting image on page {page_num + 1}: {e}")
                continue
    
    doc.close()
    return images