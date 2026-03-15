"""
Agent Runner - Orchestrates the 5-step workflow
"""
import os
import tempfile
import shutil
from pathlib import Path
from extract import extract_text_from_pdf, extract_images_from_pdf
from image_filter import filter_relevant_images
from conflict_detector import detect_conflicts
from generate_report import generate_ddr_report


def run_agent(inspection_pdf, thermal_pdf):
    """
    Main orchestrator - runs all 5 steps
    
    Args:
        inspection_pdf: Uploaded inspection PDF file
        thermal_pdf: Uploaded thermal PDF file
    
    Returns:
        dict: Contains final_report, images, and metadata
    """
    
    print("\n" + "="*80)
    print("🚀 STARTING DDR REPORT GENERATION AGENT")
    print("="*80)
    
    # ✅ FIX: Create temp directory that works on Windows, Mac, Linux
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Save uploaded files temporarily with safe filenames
        inspection_path = os.path.join(temp_dir, "inspection_report.pdf")
        thermal_path = os.path.join(temp_dir, "thermal_report.pdf")
        
        # Reset file pointers to beginning
        inspection_pdf.seek(0)
        thermal_pdf.seek(0)
        
        with open(inspection_path, "wb") as f:
            f.write(inspection_pdf.read())
        
        with open(thermal_path, "wb") as f:
            f.write(thermal_pdf.read())
        
        print(f"✅ Saved inspection report to: {inspection_path}")
        print(f"✅ Saved thermal report to: {thermal_path}")
        
        # ============================================================================
        # STEP 1: Extract Text from Both PDFs
        # ============================================================================
        print("\n📄 STEP 1: Extracting Text from PDFs...")
        print("-" * 80)
        
        inspection_text = extract_text_from_pdf(inspection_path)
        thermal_text = extract_text_from_pdf(thermal_path)
        
        print(f"✅ Inspection text extracted: {len(inspection_text)} characters")
        print(f"✅ Thermal text extracted: {len(thermal_text)} characters")
        
        # ============================================================================
        # STEP 2: Extract Images from Both PDFs
        # ============================================================================
        print("\n🖼️  STEP 2: Extracting Images from PDFs...")
        print("-" * 80)
        
        inspection_images_raw = extract_images_from_pdf(inspection_path)
        thermal_images_raw = extract_images_from_pdf(thermal_path)
        
        print(f"✅ Inspection images extracted: {len(inspection_images_raw)}")
        print(f"✅ Thermal images extracted: {len(thermal_images_raw)}")
        
        # ============================================================================
        # STEP 3: Filter Relevant Images
        # ============================================================================
        print("\n🔍 STEP 3: Filtering Relevant Images...")
        print("-" * 80)
        
        inspection_images_filtered = filter_relevant_images(inspection_images_raw)
        thermal_images_filtered = filter_relevant_images(thermal_images_raw)
        
        print(f"✅ Inspection images after filtering: {len(inspection_images_filtered)}")
        print(f"✅ Thermal images after filtering: {len(thermal_images_filtered)}")
        
        # ============================================================================
        # STEP 4: Detect Conflicts
        # ============================================================================
        print("\n⚠️  STEP 4: Detecting Conflicts...")
        print("-" * 80)
        
        conflicts = detect_conflicts(inspection_text, thermal_text)
        
        print(f"✅ Conflicts detected: {len(conflicts)}")
        for i, conflict in enumerate(conflicts, 1):
            print(f"   {i}. {conflict}")
        
        # ============================================================================
        # STEP 5: Generate DDR Report
        # ============================================================================
        print("\n📝 STEP 5: Generating DDR Report...")
        print("-" * 80)
        
        final_report = generate_ddr_report(
            inspection_text=inspection_text,
            thermal_text=thermal_text,
            conflicts=conflicts,
            num_inspection_images=len(inspection_images_filtered),
            num_thermal_images=len(thermal_images_filtered)
        )
        
        print(f"✅ DDR Report generated: {len(final_report)} characters")
        
        # Count issues and conflicts for metrics
        issues_count = final_report.count('•') + final_report.count('-')
        conflicts_count = len(conflicts)
        
        print("\n" + "="*80)
        print("✅ DDR REPORT GENERATION COMPLETE!")
        print("="*80 + "\n")
        
        # Return comprehensive result
        return {
            'final_report': final_report,
            'inspection_images': inspection_images_filtered,
            'thermal_images': thermal_images_filtered,
            'conflicts': conflicts,
            'issues_count': issues_count,
            'conflicts_count': conflicts_count,
            'inspection_text_length': len(inspection_text),
            'thermal_text_length': len(thermal_text)
        }
    
    finally:
        # ============================================================================
        # CLEANUP - Always runs even if there's an error
        # ============================================================================
        print("\n🧹 Cleaning up temporary files...")
        try:
            shutil.rmtree(temp_dir)
            print(f"✅ Deleted temp directory: {temp_dir}")
        except Exception as e:
            print(f"⚠️  Could not delete temp directory: {str(e)}")