"""
Step 4: Detect conflicts between inspection and thermal reports
"""
import os
import requests
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
        "max_tokens": 1000
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    
    data = response.json()
    return data['choices'][0]['message']['content']


def detect_conflicts(inspection_text, thermal_text):
    """
    Detect conflicts between inspection and thermal imaging reports using LLM
    
    Args:
        inspection_text: Text from inspection report
        thermal_text: Text from thermal report
    
    Returns:
        list: List of detected conflicts
    """
    
    print("\n🤖 Using LLM to detect conflicts...")
    
    # Truncate texts to avoid token limits
    inspection_sample = inspection_text[:2000]
    thermal_sample = thermal_text[:2000]
    
    prompt = f"""You are analyzing two building inspection reports for conflicts or contradictions.

**Inspection Report:**
{inspection_sample}

**Thermal Imaging Report:**
{thermal_sample}

**Task:** Identify any conflicts, contradictions, or inconsistencies between these two reports.

Examples of conflicts:
- Inspection says "no dampness" but thermal shows cold spots indicating moisture
- Inspection reports damage in Area A, but thermal shows issues in Area B
- Severity levels don't match between reports
- Temperature readings contradict visual observations

**Return format:** 
Return ONLY a JSON array of conflict strings. If no conflicts, return an empty array [].

Example: ["Inspection reports no water damage in kitchen, but thermal imaging shows temperature anomaly of 15°C indicating moisture", "Severity mismatch: Inspection rates issue as minor, thermal data suggests major problem"]

Your response (JSON array only):"""

    # Try each model in fallback list
    for model in FREE_MODELS:
        try:
            print(f"   Trying model: {model}")
            response = call_openrouter_api(prompt, model)
            print(f"   ✅ Response received from {model}")
            
            # Parse JSON response
            import json
            
            # Clean response (remove markdown code blocks if present)
            response = response.strip()
            if response.startswith('```'):
                response = response.split('```')[1]
                if response.startswith('json'):
                    response = response[4:]
            response = response.strip()
            
            conflicts = json.loads(response)
            
            if isinstance(conflicts, list):
                print(f"   ✅ Success with {model}: {len(conflicts)} conflicts found")
                return conflicts
            else:
                print(f"   ⚠️  Unexpected response format from {model}")
                continue
        
        except Exception as e:
            print(f"   ❌ Failed with {model}: {str(e)}")
            continue
    
    # If all models fail, return empty list
    print("   ⚠️  All models failed, returning no conflicts")
    return []