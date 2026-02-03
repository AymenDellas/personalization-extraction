import os
import json
from openai import OpenAI

def extract_profile_data(profile_text: str) -> dict | None:
    """
    Sends profile text to OpenRouter API to extract specific fields into JSON.
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("Error: OPENROUTER_API_KEY not found in environment variables.")
        return None

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    system_prompt = """You are an autonomous scraping and data-extraction agent.
Your job is to extract specific LinkedIn profile data into strict JSON only.
Accuracy is more important than completeness. If data is not explicitly visible, return null.
You must NOT infer, guess, or fabricate information.

Schema:
{
  "website_url": string | null
}

EXTRACTION RULES:
1. website_url: Extract personal/company website link found in Contact Info, headline, or About section. Ignore linkedin.com, twitter.com, etc. Return full URL.

CONSTRAINTS:
- Do NOT fabricate.
- Output JSON ONLY. No markdown, no preambles.
"""

    try:
        completion = client.chat.completions.create(
            model="openai/gpt-3.5-turbo", # Using a reliable efficient model via OpenRouter
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Profile Text:\n{profile_text}"}
            ],
            temperature=0, # Strict extraction
        )

        content = completion.choices[0].message.content.strip()
        
        # Helper to parse strict JSON (strip potential markdown wrapping)
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
        
        return json.loads(content)

    except Exception as e:
        print(f"Extraction error: {e}")
        return None
