
import os
import json
from openai import OpenAI

def extract_website_data(website_text: str) -> dict | None:
    """
    Analyzes website text using the user-defined schema to extract Key Landing Page elements.
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("Error: OPENROUTER_API_KEY not found.")
        return None

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    system_prompt = """You are an expert landing page analyst.
Analyze the Provided Website Content to extract strategic insights.

Return STRICT JSON using the schema below.

SCHEMA:
{
  "direct_goal": string | null,
  "primary_cta_text": string | null,
  "cta_destination": "calendar" | "form" | "email" | "external" | null,
  "all_ctas_found": [string],
  "roadblock": string | null,
  "audience": string | null
}

PROCESS FOR PRIMARY CTA IDENTIFICATION:
1. Scan the text for ALL potential Call-to-Action (CTA) elements (buttons, links, form submits).
2. List them in "all_ctas_found".
3. COMPARE all found CTAs to identify the PRIMARY one. 
   - The primary CTA is typically the one that appears first (above the fold), is repeated most often, or represents the highest level of commitment (e.g., "Book a Call" usually beats "Learn More").
   - Identify its exact text for "primary_cta_text".
   - Determine its destination type for "cta_destination".

DEFINITIONS:

- direct_goal:
  The ultimate conversion goal based on the primary CTA (e.g., "Schedule a sales demo", "Get a free audit").

- primary_cta_text:
  The text of the single most prominent CTA identified in Step 3 of the process.

- cta_destination:
  Where that primary CTA leads.

- roadblock:
  Friction points (e.g., "Wall of text", "Missing testimonials", "Complex 10-field form").

- audience:
  The specific persona targeted (e.g., "E-commerce store owners", "Founders of Series A startups").

CONSTRAINTS:
- Be analytical and precise.
- Output JSON ONLY.
"""

    try:
        # Truncate text to avoid token limits if necessary (e.g. 15k chars is usually safe for context)
        truncated_text = website_text[:15000]

        completion = client.chat.completions.create(
            model="openai/gpt-3.5-turbo", # or a comparable model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Website Content:\n{truncated_text}"}
            ],
            temperature=0, 
        )

        content = completion.choices[0].message.content.strip()
        
        # Helper to parse strict JSON (strip potential markdown wrapping)
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
        
        return json.loads(content)

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Website Extraction error: {e}")
        return None
