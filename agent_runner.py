from tools import (
    extract_text_tool,
    extract_images_tool,
    filter_images_tool,
    conflict_detection_tool,
    ddr_generation_tool
)


def run_agent(inspection_file, thermal_file):
    """Main agent workflow for DDR generation."""
    
    steps = []
    
    # Step 1: Extract text
    steps.append("Step 1: Extracting text from both reports...")
    inspection_text = extract_text_tool(inspection_file)
    thermal_text = extract_text_tool(thermal_file)
    steps.append("✓ Text extraction completed")
    
    # Step 2: Extract images
    steps.append("Step 2: Extracting images from PDFs...")
    inspection_images = extract_images_tool(inspection_file)
    thermal_images = extract_images_tool(thermal_file)
    steps.append(f"✓ Found {len(inspection_images)} inspection images, {len(thermal_images)} thermal images")
    
    # Step 3: Filter relevant images
    steps.append("Step 3: Filtering relevant images...")
    inspection_images = filter_images_tool(inspection_images)
    thermal_images = filter_images_tool(thermal_images)
    steps.append(f"✓ Filtered to {len(inspection_images)} inspection images, {len(thermal_images)} thermal images")
    
    # Step 4: Detect conflicts
    steps.append("Step 4: Detecting conflicts between reports...")
    conflicts = conflict_detection_tool(inspection_text, thermal_text)
    steps.append("✓ Conflict detection completed")
    
    # Step 5: Generate DDR
    steps.append("Step 5: Generating DDR report...")
    report = ddr_generation_tool(
        inspection_text,
        thermal_text,
        conflicts,
        len(inspection_images),
        len(thermal_images)
    )
    steps.append("✓ DDR report generated successfully")
    
    return report, inspection_images, thermal_images, steps