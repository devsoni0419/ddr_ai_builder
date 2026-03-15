import streamlit as st
from agent_runner import run_agent
from PIL import Image
import re

st.set_page_config(page_title="AI DDR Report Generator", layout="wide")

st.title("🏗️ AI DDR Report Generator")
st.markdown("### Automated Detailed Diagnostic Report Generation")

col1, col2 = st.columns(2)

with col1:
    inspection_file = st.file_uploader("📄 Upload Inspection Report", type=["pdf"])

with col2:
    thermal_file = st.file_uploader("🌡️ Upload Thermal Report", type=["pdf"])


def render_report(report, inspection_images, thermal_images):
    """Render the DDR report with images placed at appropriate markers."""
    
    inspection_index = 0
    thermal_index = 0
    
    # Split report into lines
    lines = report.split('\n')
    
    for line in lines:
        # Check for image markers
        if '[INSPECTION_IMAGE]' in line:
            if inspection_index < len(inspection_images):
                img_data = inspection_images[inspection_index]
                img_data['image'].seek(0)
                img = Image.open(img_data['image'])
                st.image(img, caption=f"Inspection Image {inspection_index + 1}", width=450)
                inspection_index += 1
            else:
                st.warning("⚠️ Inspection Image Not Available")
        
        elif '[THERMAL_IMAGE]' in line:
            if thermal_index < len(thermal_images):
                img_data = thermal_images[thermal_index]
                img_data['image'].seek(0)
                img = Image.open(img_data['image'])
                st.image(img, caption=f"Thermal Image {thermal_index + 1}", width=450)
                thermal_index += 1
            else:
                st.warning("⚠️ Thermal Image Not Available")
        
        else:
            # Regular text line
            if line.strip():
                st.markdown(line)


if inspection_file and thermal_file:
    
    if st.button("🚀 Generate DDR Report", type="primary"):
        
        with st.spinner("🤖 AI Agent is processing your reports..."):
            
            try:
                report, inspection_images, thermal_images, steps = run_agent(
                    inspection_file,
                    thermal_file
                )
                
                # Show workflow steps
                st.success("✅ Report Generated Successfully!")
                
                with st.expander("📋 View Agent Workflow Steps"):
                    for step in steps:
                        st.write(step)
                
                st.divider()
                
                # Render the report
                st.subheader("📊 Generated DDR Report")
                render_report(report, inspection_images, thermal_images)
                
                # Download option
                st.divider()
                st.download_button(
                    label="📥 Download Report (Text)",
                    data=report,
                    file_name="DDR_Report.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.exception(e)

else:
    st.info("👆 Please upload both Inspection Report and Thermal Report to begin.")