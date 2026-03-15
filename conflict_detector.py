import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()


def detect_conflicts(inspection_text, thermal_text):
    """Use LLM to detect conflicts between inspection and thermal reports."""
    
    api_key = os.getenv("OPEN_ROUTER_API_KEY")
    base_url = os.getenv("OPEN_ROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    
    if not api_key:
        print("Warning: OPEN_ROUTER_API_KEY not found")
        return "[]"
    
    prompt = f"""You are analyzing two building inspection reports for conflicts or contradictions.

INSPECTION REPORT:
{inspection_text[:3000]}

THERMAL REPORT:
{thermal_text[:3000]}

Task: Identify any conflicts, contradictions, or inconsistencies between these two reports.

Examples of conflicts:
- Inspection says "no moisture detected" but thermal shows cold spots indicating moisture
- Inspection says "wall is dry" but thermal shows temperature anomalies
- Different severity assessments for the same area

Return your response as a JSON array of conflict objects. Each conflict should have:
- "area": the location/area where conflict occurs
- "inspection_finding": what the inspection report states
- "thermal_finding": what the thermal report states
- "conflict_description": brief description of the contradiction

If no conflicts found, return an empty array: []

Response (JSON only, no markdown):"""

    try:
        response = requests.post(
            f"{base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:8501",
                "X-Title": "DDR Conflict Detector"
            },
            json={
                "model": "deepseek/deepseek-chat",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.1,
                "max_tokens": 2000
            },
            timeout=60
        )
        
        response.raise_for_status()
        result = response.json()
        
        content = result['choices'][0]['message']['content'].strip()
        
        # Clean up markdown if present
        if content.startswith("```json"):
            content = content.replace("```json", "").replace("```", "").strip()
        
        return content
        
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error detecting conflicts: {e}")
        print(f"Response: {response.text if 'response' in locals() else 'No response'}")
        return "[]"
    except Exception as e:
        print(f"Error detecting conflicts: {e}")
        return "[]"