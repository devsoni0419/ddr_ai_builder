from extract import extract_pdf_text, extract_images_from_pdf
from image_filter import filter_relevant_images
from conflict_detector import detect_conflicts
from generate_report import generate_ddr


def extract_text_tool(file):
    """Extract text from PDF file."""
    return extract_pdf_text(file)


def extract_images_tool(file):
    """Extract images from PDF file."""
    return extract_images_from_pdf(file)


def filter_images_tool(images):
    """Filter relevant images from extracted images."""
    return filter_relevant_images(images)


def conflict_detection_tool(inspection_text, thermal_text):
    """Detect conflicts between inspection and thermal reports."""
    return detect_conflicts(inspection_text, thermal_text)


def ddr_generation_tool(inspection_text, thermal_text, conflicts, num_inspection_images, num_thermal_images):
    """Generate DDR report."""
    return generate_ddr(
        inspection_text,
        thermal_text,
        conflicts,
        num_inspection_images,
        num_thermal_images
    )