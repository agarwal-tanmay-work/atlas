from google import genai
from google.genai import types
import json
import uuid
from config import GEMINI_API_KEY
from models.schemas import FailureRecord

client = genai.Client(api_key=GEMINI_API_KEY)

EXTRACTION_PROMPT = """
You are an expert failure analyst. You will be given raw text describing a failure, incident, post-mortem, or disaster. Your job is to extract structured information from it.

Return ONLY a valid JSON object with EXACTLY these fields. Do not include any explanation or markdown. Only raw JSON.

{{
  "title": "Short descriptive title of what failed (max 10 words)",
  "domain": "One of: Software Engineering, Aviation, Finance, Healthcare, Government, Military, Infrastructure, Manufacturing, Space, Cybersecurity",
  "subdomain": "More specific area within the domain",
  "year": 0, // integer year when this happened
  "organization": "Name of company/organization involved or null",
  "what_failed": "1-2 sentences describing what actually broke or went wrong",
  "root_cause": "The true underlying cause, not just the symptom",
  "root_cause_category": "MUST be exactly one of: Communication Breakdown, Single Point of Failure, Incentive Misalignment, Over-Complexity, Ignored Warning Signs, Human Error, Process Failure, Technical Debt, Scaling Failure, Security Negligence, Leadership Failure, External Dependency Failure",
  "warning_signs": ["list", "of", "warning signs that were present but ignored"],
  "what_was_done_wrong": "A clear explanation of the decisions or actions that led to failure",
  "how_it_was_fixed": "How it was resolved, or null if not applicable",
  "lesson": "The single most important lesson someone should take away from this failure",
  "severity": "One of: Low, Medium, High, Critical",
  "tags": ["relevant", "tags", "for", "categorization"]
}}

Raw text to analyze:
{raw_text}
"""

def extract_failure_from_text(
    raw_text: str, source_url: str = None
) -> FailureRecord | None:
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=EXTRACTION_PROMPT.format(raw_text=raw_text[:4000]),
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            ),
        )

        content = response.text.strip()
        data = json.loads(content)
        data["id"] = str(uuid.uuid4())
        data["source_url"] = source_url
        data["related_failure_ids"] = []

        return FailureRecord(**data)
    except Exception as e:
        print(f"Extraction failed: {e}")
        return None
