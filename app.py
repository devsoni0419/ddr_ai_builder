import streamlit as st
from agent_runner import run_agent
import base64
from pathlib import Path

# ✅ Page Configuration
st.set_page_config(
    page_title="DDR Report Generator",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ✅ Custom CSS for Professional Styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    h1 {
        color: #1f77b4;
        border-bottom: 3px solid #1f77b4;
        padding-bottom: 10px;
        margin-bottom: 2rem;
    }
    h2 {
        color: #ff7f0e;
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #ff7f0e;
    }
    h3 {
        color: #2ca02c;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    .stImage {
        border: 2px solid #e0e0e0;
        border-radius: 8px;
        padding: 10px;
        margin: 15px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .reportSection {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .stAlert {
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)


def display_report_with_images(report_text, inspection_images, thermal_images):
    """Display report with properly formatted images and sections"""
    
    inspection_idx = 0
    thermal_idx = 0
    current_section = "General"
    
    lines = report_text.split('\n')
    
    for line in lines:
        # Track current section for better image captions
        if line.startswith('## '):
            current_section = line.replace('## ', '').strip()
            st.markdown(f"## {current_section}")
            continue
        elif line.startswith('### '):
            current_section = line.replace('### ', '').strip()
            st.markdown(f"### {current_section}")
            continue
        
        # Handle inspection image markers
        if '[INSPECTION_IMAGE]' in line:
            # Display the observation text without the marker
            observation_text = line.replace('[INSPECTION_IMAGE]', '').strip()
            if observation_text:
                st.markdown(f"**{observation_text}**")
            
            # Display the image
            if inspection_idx < len(inspection_images):
                col1, col2, col3 = st.columns([1, 3, 1])
                with col2:
                    st.image(
                        inspection_images[inspection_idx],
                        caption=f'📸 Inspection Image {inspection_idx + 1} - {current_section}',
                        use_column_width=True
                    )
                inspection_idx += 1
        
        # Handle thermal image markers
        elif '[THERMAL_IMAGE]' in line:
            # Display the observation text without the marker
            observation_text = line.replace('[THERMAL_IMAGE]', '').strip()
            if observation_text:
                st.markdown(f"**{observation_text}**")
            
            # Display the image
            if thermal_idx < len(thermal_images):
                col1, col2, col3 = st.columns([1, 3, 1])
                with col2:
                    st.image(
                        thermal_images[thermal_idx],
                        caption=f'🌡️ Thermal Image {thermal_idx + 1} - {current_section}',
                        use_column_width=True
                    )
                thermal_idx += 1
        
        # Regular text lines
        else:
            if line.strip():  # Only display non-empty lines
                st.markdown(line)


def create_download_link(report_text, filename="DDR_Report.md"):
    """Create a download link for the report"""
    b64 = base64.b64encode(report_text.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{filename}">📥 Download Report</a>'


def main():
    # Header
    st.title("🏗️ AI DDR Report Generator")
    st.markdown("**Automated Detailed Diagnostic Report Generation from Building Inspection & Thermal Imaging**")
    st.markdown("---")
    
    # Sidebar Instructions
    with st.sidebar:
        st.header("📖 Instructions")
        st.markdown("""
        ### How to Use:
        1. **Upload Inspection Report** (PDF)
        2. **Upload Thermal Report** (PDF)
        3. Click **Generate DDR Report**
        4. Review the generated report
        5. Download if needed
        
        ### Report Includes:
        - ✅ Property Issue Summary
        - ✅ Area-wise Observations
        - ✅ Root Cause Analysis
        - ✅ Severity Assessment
        - ✅ Recommended Actions
        - ✅ Conflict Detection
        - ✅ Missing Information Handling
        
        ### Supported Formats:
        - PDF files only
        - Max size: 200MB per file
        """)
        
        st.markdown("---")
        st.info("💡 **Tip:** Ensure PDFs contain clear text and images for best results.")
    
    # Main Content Area
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📄 Upload Inspection Report")
        inspection_file = st.file_uploader(
            "Choose Inspection PDF",
            type=['pdf'],
            help="Upload the building inspection report PDF"
        )
        if inspection_file:
            st.success(f"✅ Loaded: {inspection_file.name}")
    
    with col2:
        st.subheader("🌡️ Upload Thermal Report")
        thermal_file = st.file_uploader(
            "Choose Thermal PDF",
            type=['pdf'],
            help="Upload the thermal imaging report PDF"
        )
        if thermal_file:
            st.success(f"✅ Loaded: {thermal_file.name}")
    
    st.markdown("---")
    
    # Generate Button
    if inspection_file and thermal_file:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            generate_button = st.button(
                "🔍 Generate DDR Report",
                type="primary",
                use_container_width=True
            )
        
        if generate_button:
            # Progress indicators
            with st.spinner("🤖 Processing reports..."):
                try:
                    # Run the agent
                    result = run_agent(inspection_file, thermal_file)
                    
                    # Success message
                    st.success("✅ DDR Report Generated Successfully!")
                    
                    # Display metrics
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("📸 Inspection Images", len(result.get('inspection_images', [])))
                    with col2:
                        st.metric("🌡️ Thermal Images", len(result.get('thermal_images', [])))
                    with col3:
                        st.metric("⚠️ Issues Detected", result.get('issues_count', 'N/A'))
                    with col4:
                        st.metric("🔍 Conflicts Found", result.get('conflicts_count', 'N/A'))
                    
                    st.markdown("---")
                    
                    # Display the report
                    st.markdown("## 📋 Generated Detailed Diagnostic Report (DDR)")
                    st.markdown("---")
                    
                    display_report_with_images(
                        result['final_report'],
                        result.get('inspection_images', []),
                        result.get('thermal_images', [])
                    )
                    
                    # Download Section
                    st.markdown("---")
                    st.markdown("### 💾 Download Report")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            label="📥 Download as Markdown (.md)",
                            data=result['final_report'],
                            file_name="DDR_Report.md",
                            mime="text/markdown",
                            use_container_width=True
                        )
                    with col2:
                        st.download_button(
                            label="📥 Download as Text (.txt)",
                            data=result['final_report'],
                            file_name="DDR_Report.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                
                except Exception as e:
                    st.error(f"❌ Error generating report: {str(e)}")
                    st.exception(e)
    
    else:
        st.warning("⚠️ Please upload both Inspection and Thermal reports to continue.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #666;'>
            <p>🏗️ DDR Report Generator | Built with Streamlit & AI</p>
            <p>For building inspection professionals</p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()