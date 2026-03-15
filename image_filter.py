from PIL import Image
import io


def filter_relevant_images(images):
    """Filter out irrelevant images (logos, small graphics)."""
    relevant = []
    
    for img_data in images:
        try:
            img_data['image'].seek(0)
            img = Image.open(img_data['image'])
            
            width = img_data['width']
            height = img_data['height']
            
            # Filter criteria
            is_large_enough = width >= 300 and height >= 300
            is_reasonable_aspect = 0.3 <= (width / height) <= 3.0
            
            # Check if image has sufficient content (not mostly white/blank)
            img_gray = img.convert('L')
            pixels = list(img_gray.getdata())
            avg_brightness = sum(pixels) / len(pixels)
            has_content = avg_brightness < 240  # Not mostly white
            
            if is_large_enough and is_reasonable_aspect and has_content:
                img_data['image'].seek(0)
                relevant.append(img_data)
            
        except Exception as e:
            print(f"Error filtering image: {e}")
            continue
    
    return relevant