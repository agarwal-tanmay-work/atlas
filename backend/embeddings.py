from google import genai
from google.genai import types
from models.schemas import FailureRecord
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

def embed_text(text: str) -> list[float]:
    """Generate embedding using Google Gemini explicitly truncated to 384 dimensions to match DB schemas natively."""
    result = client.models.embed_content(
        model="gemini-embedding-2-preview",
        contents=text,
        config=types.EmbedContentConfig(output_dimensionality=384)
    )
    return result.embeddings[0].values

def embed_failure(failure: FailureRecord) -> list[float]:
    """Generate a semantic combination layout of the failure."""
    content = f"Title: {failure.title}\nDomain: {failure.domain}\nWhat Failed: {failure.what_failed}\nRoot Cause: {failure.root_cause_category}\nLesson: {failure.lesson}"
    return embed_text(content)
