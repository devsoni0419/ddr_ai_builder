"""
Tool wrapper functions for the agent
These wrap the core extraction, filtering, and generation logic
"""
from extract import extract_text_from_pdf, extract_images_from_pdf
from image_filter import filter_relevant_images
from conflict_detector import detect_conflicts
from generate_report import generate_ddr_report


def extract_text_tool(pdf_path):
    """Wrapper for text extraction"""
    return extract_text_from_pdf(pdf_path)


def extract_images_tool(pdf_path):
    """Wrapper for image extraction"""
    return extract_images_from_pdf(pdf_path)


def filter_images_tool(images):
    """Wrapper for image filtering"""
    return filter_relevant_images(images)


def detect_conflicts_tool(inspection_text, thermal_text):
    """Wrapper for conflict detection"""
    return detect_conflicts(inspection_text, thermal_text)


def generate_report_tool(inspection_text, thermal_text, conflicts, num_inspection_images, num_thermal_images):
    """Wrapper for report generation"""
    return generate_ddr_report(
        inspection_text,
        thermal_text,
        conflicts,
        num_inspection_images,
        num_thermal_images
    )