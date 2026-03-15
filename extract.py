"""
Steps 1 & 2: Extract text and images from PDFs
"""

import fitz
import io
from PIL import Image


def extract_text_from_pdf(pdf_path):

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


def extract_images_from_pdf(pdf_path, min_size=300):
    import fitz
    import io
    from PIL import Image

    images = []

    doc = fitz.open(pdf_path)

    for page_index in range(len(doc)):
        page = doc.load_page(page_index)
        image_list = page.get_images(full=True)

        print(f"Page {page_index+1}: {len(image_list)} raw images found")

        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            image = Image.open(io.BytesIO(image_bytes))

            width, height = image.size

            # 🔹 FILTER SMALL ICONS
            if width < min_size or height < min_size:
                continue

            images.append(image)

            print(f"Saved image {img_index+1}: {width}x{height}")

    print(f"Total filtered images: {len(images)}")

    return images