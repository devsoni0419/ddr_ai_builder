import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

SYSTEM_PROMPT = """You are a professional building inspection expert generating a Detailed Diagnostic Report (DDR).

You must create a comprehensive, client-friendly report with the following EXACT structure:

# 1. Property Issue Summary
Provide a high-level summary of all identified issues.

# 2. Area-wise Observations
List observations organized by location/area. For each area, combine findings from both visual inspection and thermal imaging.

After each observation that references an image, include EXACTLY one of these markers:
- [INSPECTION_IMAGE] - for visual inspection photos
- [THERMAL_IMAGE] - for thermal imaging photos

Place markers on a new line immediately after the relevant observation.

# 3. Probable Root Cause
Explain the likely underlying causes of the observed issues.

# 4. Severity Assessment
Rate the severity (Low/Medium/High/Critical) with clear reasoning.

# 5. Recommended Actions
Provide prioritized action items for remediation.

# 6. Additional Notes
Include any supplementary information or considerations.

# 7. Missing or Unclear Information
Explicitly list what information is "Not Available" or unclear.

# 8. Conflicting Information
Document any contradictions between reports.

CRITICAL RULES:
- Do NOT invent facts not present in the source documents
- If information is missing, write "Not Available"
- Use simple, client-friendly language
- Avoid unnecessary technical jargon
- Use [INSPECTION_IMAGE] and [THERMAL_IMAGE] markers where images should appear
- Only place image markers where there is a specific observation that would benefit from visual evidence
"""


def generate_ddr(inspection_text, thermal_text, conflicts, num_inspection_images, num_thermal_images):
    """Generate the DDR report using LLM."""
    
    api_key = os.getenv("OPEN_ROUTER_API_KEY")
    base_url = os.getenv("OPEN_ROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    
    if not api_key:
        return "Error: OPEN_ROUTER_API_KEY not found in environment variables"
    
    prompt = f"""Generate a Detailed Diagnostic Report (DDR) based on the following information:

INSPECTION REPORT:
{inspection_text}

THERMAL REPORT:
{thermal_text}

DETECTED CONFLICTS:
{conflicts}

AVAILABLE IMAGES:
- {num_inspection_images} inspection images available
- {num_thermal_images} thermal images available

Generate the complete DDR following the required structure. Use image markers [INSPECTION_IMAGE] and [THERMAL_IMAGE] strategically where visual evidence would support findings.
"""

    try:
        response = requests.post(
            f"{base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:8501",
                "X-Title": "DDR Report Generator"
            },
            json={
                "model": "deepseek/deepseek-chat",
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3,
                "max_tokens": 4000
            },
            timeout=120
        )
        
        response.raise_for_status()
        result = response.json()
        
        return result['choices'][0]['message']['content']
        
    except requests.exceptions.HTTPError as e:
        error_msg = f"HTTP Error: {e}"
        if 'response' in locals():
            error_msg += f"\nResponse: {response.text}"
        print(error_msg)
        return f"Error generating report: {error_msg}"
    except Exception as e:
        print(f"Unexpected error: {e}")
        return f"Error generating report: {str(e)}"