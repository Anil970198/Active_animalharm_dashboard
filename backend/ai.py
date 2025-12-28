import os
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")

# Initialize OpenRouter Client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

def extract_violation_with_llm(text_chunk):
    """
    Uses an LLM via OpenRouter to extract structured violation data.
    """
    if not OPENROUTER_API_KEY or OPENROUTER_API_KEY.startswith("your_key"):
        print("Warning: OPENROUTER_API_KEY not configured. Skipping AI extraction.")
        return None

    prompt = f"""
    You are an expert data extractor. Analyze the following text from an enforcement report PDF.
    Extract the following fields if present:
    - facility_name: Name of the farm or facility.
    - violation_date: Date of the violation (YYYY-MM-DD).
    - violation_type: Brief description of the violation (e.g., "Inhumane handling", "Pollution").
    - location: City and State (e.g., "Springfield, IL").
    - summary: A 1-sentence summary of what happened.

    Return valid JSON only. If no specific violation is clearly described, return {{"found": false}}.
    
    Text:
    {text_chunk[:3000]}
    """
    
    try:
        response = client.chat.completions.create(
            model=OPENROUTER_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts data and outputs raw JSON."},
                {"role": "user", "content": prompt}
            ],
            extra_headers={
                "HTTP-Referer": "http://localhost:3000",
                "X-Title": "Transparency Dashboard"
            }
        )
        content = response.choices[0].message.content.strip()
        
        # Clean markdown code blocks if present
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
            
        return json.loads(content)
    except Exception as e:
        print(f"AI Extraction failed: {e}")
        return None
