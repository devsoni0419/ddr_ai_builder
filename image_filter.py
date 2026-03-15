"""
Step 3: Filter relevant images from extracted images
"""
from PIL import Image
import io


def filter_relevant_images(images):
    """
    Filter extracted images to keep only relevant ones
    
    Filtering criteria:
    1. Minimum size (300x300 pixels)
    2. Reasonable aspect ratio (0.3 to 3.0)
    3. Not blank/white pages (average brightness < 240)
    
    Args:
        images: List of image dictionaries from extract.py
    
    Returns:
        list: Filtered list of relevant images (as file paths or PIL Image objects)
    """
    
    print(f"\n🔍 Filtering {len(images)} images...")
    
    relevant_images = []
    
    for i, img_data in enumerate(images):
        try:
            # Get image properties
            width = img_data['width']
            height = img_data['height']
            image_bytes = img_data['image']
            
            # Filter 1: Minimum size
            if width < 300 or height < 300:
                print(f"   ❌ Image {i+1}: Too small ({width}x{height})")
                continue
            
            # Filter 2: Aspect ratio
            aspect_ratio = width / height
            if aspect_ratio < 0.3 or aspect_ratio > 3.0:
                print(f"   ❌ Image {i+1}: Bad aspect ratio ({aspect_ratio:.2f})")
                continue
            
            # Filter 3: Check if not blank (brightness check)
            img = Image.open(io.BytesIO(image_bytes))
            img_gray = img.convert('L')
            pixels = list(img_gray.getdata())
            avg_brightness = sum(pixels) / len(pixels)
            
            if avg_brightness > 240:  # Too bright = likely blank page
                print(f"   ❌ Image {i+1}: Likely blank page (brightness: {avg_brightness:.1f})")
                continue
            
            # Image passed all filters
            print(f"   ✅ Image {i+1}: KEPT ({width}x{height}, brightness: {avg_brightness:.1f})")
            relevant_images.append(img)
        
        except Exception as e:
            print(f"   ⚠️  Image {i+1}: Error during filtering - {str(e)}")
            continue
    
    print(f"\n✅ Filtering complete: {len(relevant_images)} relevant images kept")
    
    return relevant_images