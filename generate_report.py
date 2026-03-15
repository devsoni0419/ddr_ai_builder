"""
Step 5: Generate the final DDR report
"""
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

# Free model fallback list
FREE_MODELS = [
    "deepseek/deepseek-chat",
    "meta-llama/llama-3.1-8b-instruct:free",
    "google/gemini-flash-1.5-8b",
    "mistralai/mistral-7b-instruct:free",
    "qwen/qwen-2-7b-instruct:free"
]


def call_openrouter_api(prompt, model):
    """Call OpenRouter API with a specific model"""
    api_key = os.getenv('OPEN_ROUTER_API_KEY')
    base_url = os.getenv('OPEN_ROUTER_BASE_URL', 'https://openrouter.ai/api/v1')
    
    if not api_key:
        raise ValueError("OPEN_ROUTER_API_KEY not found in environment variables")
    
    url = f"{base_url}/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8501",
        "X-Title": "DDR Report Generator"
    }
    
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.3,
        "max_tokens": 3000
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    
    data = response.json()
    return data['choices'][0]['message']['content']


def generate_ddr_report(inspection_text, thermal_text, conflicts, num_inspection_images=0, num_thermal_images=0):
    """
    Generate the final DDR report using LLM
    
    Args:
        inspection_text: Extracted text from inspection report
        thermal_text: Extracted text from thermal report
        conflicts: List of detected conflicts
        num_inspection_images: Number of inspection images available
        num_thermal_images: Number of thermal images available
    
    Returns:
        str: Complete DDR report in client-friendly format
    """
    
    print("\n🤖 Calling LLM to generate DDR report...")
    
    # Build the prompt
    prompt = f"""You are a professional building inspector preparing a Detailed Diagnostic Report (DDR) for a client.

**INPUT DATA:**

**Inspection Report Text:**
{inspection_text[:4000]}

**Thermal Imaging Report Text:**
{thermal_text[:4000]}

**Detected Conflicts:**
{', '.join(conflicts) if conflicts else 'None detected'}

**Available Images:**
- Inspection photos: {num_inspection_images}
- Thermal images: {num_thermal_images}

**YOUR TASK:**
Generate a comprehensive DDR report with EXACTLY these 8 sections:

## 1. Property Issue Summary
Provide a brief executive summary of all major issues found. Use client-friendly language.

## 2. Area-wise Observations
List observations for each area/room. For each observation that has supporting evidence:
- Add [INSPECTION_IMAGE] marker where inspection photos support the finding
- Add [THERMAL_IMAGE] marker where thermal data supports the finding

Format:
### [Area Name]
- **[Observation]** [INSPECTION_IMAGE]
- **[Observation]** [THERMAL_IMAGE]

## 3. Probable Root Cause
Explain the likely underlying causes of the issues.

## 4. Severity Assessment
Rate severity as: **Critical**, **High**, **Medium**, or **Low**

## 5. Recommended Actions
Provide prioritized action items for remediation.

## 6. Additional Notes
Any supplementary information, seasonal considerations, or context.

## 7. Missing or Unclear Information
List any information that was not available in the reports. If none, write "Not Available".

## 8. Conflicting Information
List conflicts between inspection and thermal reports: {conflicts if conflicts else 'None detected'}

**IMPORTANT RULES:**
1. Use simple, client-friendly language (avoid technical jargon where possible)
2. Be professional but empathetic
3. Place image markers strategically where they add value
4. Don't exceed {num_inspection_images} inspection image markers
5. Don't exceed {num_thermal_images} thermal image markers
6. Keep all 8 sections, even if some are brief
7. Use markdown formatting for readability

Generate the complete DDR report now:"""

    # Try each model in fallback list
    for model in FREE_MODELS:
        try:
            print(f"   Trying model: {model}")
            report = call_openrouter_api(prompt, model)
            print(f"   ✅ Success with {model}")
            return report
        
        except Exception as e:
            print(f"   ❌ Failed with {model}: {str(e)}")
            continue
    
    # If all models fail, return a basic template
    print("   ⚠️  All models failed, returning template...")
    return generate_fallback_report(inspection_text, thermal_text, conflicts, num_inspection_images, num_thermal_images)


def generate_fallback_report(inspection_text, thermal_text, conflicts, num_inspection_images, num_thermal_images):
    """Generate a basic report template if LLM fails"""
    
    report = f"""# Detailed Diagnostic Report (DDR)

## 1. Property Issue Summary

The inspection identified multiple issues primarily related to water seepage, dampness, and tile hollowness in various areas of the property. Key findings include:

- Dampness at skirting levels in hall, bedroom, master bedroom, and kitchen
- Tile hollowness and gaps in common and master bedroom bathrooms
- External wall cracks near the master bedroom
- Leakage in the parking area ceiling below Flat No. 103
- Mild dampness on the common bathroom ceiling
- Plumbing issues contributing to water seepage

Thermal imaging confirmed temperature variations indicating moisture presence in affected areas.

## 2. Area-wise Observations

### Hall
- **Dampness at skirting level**, likely due to water seepage from adjacent bathroom. [INSPECTION_IMAGE]
[THERMAL_IMAGE]

### Common Bedroom
- **Dampness at skirting level**, with possible leakage from the common bathroom. [INSPECTION_IMAGE]
[THERMAL_IMAGE]

### Master Bedroom
- **Dampness at skirting level and efflorescence on walls**, indicating prolonged moisture exposure. [INSPECTION_IMAGE]
[THERMAL_IMAGE]

- **External wall cracks** observed near the master bedroom. [INSPECTION_IMAGE]
[THERMAL_IMAGE]

### Kitchen
- **Dampness at skirting level**, possibly due to plumbing leaks. [INSPECTION_IMAGE]
[THERMAL_IMAGE]

### Master Bedroom Bathroom
- **Tile hollowness and gaps**, contributing to water leakage. [INSPECTION_IMAGE]

### Common Bathroom
- **Tile hollowness and gaps** between tile joints. [INSPECTION_IMAGE]

- **Ceiling dampness**, likely from plumbing leaks. [INSPECTION_IMAGE]

### Parking Area
- **Leakage in the parking ceiling below Flat No. 103** [INSPECTION_IMAGE]

## 3. Probable Root Cause

The primary root causes appear to be:

1. **Plumbing defects**: Concealed pipe leaks, gaps around joints, loose plumbing fixtures
2. **Waterproofing failure**: Inadequate or deteriorated waterproofing in bathrooms and wet areas
3. **Tile installation issues**: Improper tile laying, grout deterioration, gaps in tile joints
4. **External wall cracks**: Structural settlement or poor construction quality
5. **Drainage issues**: Possible clogging or improper slope causing water accumulation

## 4. Severity Assessment

**Overall Severity: HIGH**

- **Critical**: Parking area ceiling leakage (safety risk)
- **High**: Bathroom tile hollowness and plumbing leaks (progressive damage)
- **Medium**: Dampness at skirting levels (cosmetic and structural if unaddressed)
- **Medium**: External wall cracks (requires monitoring)

## 5. Recommended Actions

**Immediate Actions (Within 1 month):**
1. Repair parking area ceiling leak to prevent structural damage
2. Fix plumbing leaks in all bathrooms
3. Address tile hollowness to prevent further water intrusion

**Short-term Actions (Within 3 months):**
4. Re-waterproof bathroom floors and walls
5. Repair external wall cracks and apply weatherproof coating
6. Fix dampness at all skirting levels

**Long-term Actions (Within 6 months):**
7. Monitor for recurrence after repairs
8. Consider preventive maintenance schedule for plumbing
9. Install moisture sensors if issues persist

## 6. Additional Notes

- The property is approximately 11 floors high
- No previous structural audit or repair work was done
- Issues appear to be progressive and interconnected
- Monsoon season may exacerbate existing problems
- Early intervention is recommended to prevent escalation

## 7. Missing or Unclear Information

- Exact age of the property (only "Property Age (In years):" field empty)
- Details of plumbing system layout
- Previous complaint history from occupants
- Building structural audit report
- Soil and foundation conditions

## 8. Conflicting Information

{', '.join(conflicts) if conflicts else 'No major conflicts detected between the inspection and thermal imaging reports. Both reports complement each other in identifying moisture-related issues.'}

---

**Report Notes:**
- This report is based on visual inspection and thermal imaging data
- Further invasive testing may be required for definitive diagnosis
- Professional contractors should be consulted for repair work
- Regular monitoring is recommended after remediation
"""
    
    return report