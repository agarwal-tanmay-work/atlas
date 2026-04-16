from fastapi import APIRouter
import json
from google import genai
from google.genai import types

from config import GEMINI_API_KEY
from embeddings import embed_text
from database import search_by_embedding, get_failure_by_id
from models.schemas import AnalyzeRequest, AnalyzeResponse

router = APIRouter()
client = genai.Client(api_key=GEMINI_API_KEY)

@router.post("", response_model=AnalyzeResponse)
def analyze_project(request: AnalyzeRequest):
    # 1. Embed the project description
    query_emb = embed_text(request.project_description)
    
    # 2. Query database for top 8 similar failures
    results = search_by_embedding(query_emb, n_results=8)
    
    # 3. Fetch full records
    top_failures = []
    for res in results:
        f = get_failure_by_id(res["id"])
        if f:
            top_failures.append(f)
            
    # Format failures for prompt
    formatted_failures = ""
    for f in top_failures:
        formatted_failures += f"\n- Title: {f.title}\nDomain: {f.domain}\nRoot Cause: {f.root_cause_category}\nWhat Failed: {f.what_failed}\nLesson: {f.lesson}\n"
    
    # 4. Prompt to Gemini
    prompt = f"""
You are a world-class failure analyst. A person is about to build the following project:

PROJECT: {request.project_description}

Based on historical failure records, here are the most analogous past failures:

{formatted_failures}

Using these historical patterns, provide your analysis in the following JSON format ONLY (no markdown, no explanation, no backticks, ONLY a JSON object):

{{
  "risk_summary": "2-3 paragraph analysis of why projects like this fail and what makes this one risky or safe",
  "most_likely_root_causes": ["top 4 root cause categories most likely to affect this project, in order of likelihood"],
  "warning_signs_to_watch": ["6-8 specific, concrete warning signs this team should watch for"],
  "recommended_mitigations": ["5-7 specific, actionable recommendations to reduce failure risk"],
  "overall_risk_level": "Low or Medium or High or Critical"
}}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            )
        )
        
        reply = response.text.strip()
        data = json.loads(reply)
        
        return AnalyzeResponse(
            project_description=request.project_description,
            risk_summary=data.get("risk_summary", "Analysis available."),
            top_analogous_failures=top_failures[:4], # Return top 4
            most_likely_root_causes=data.get("most_likely_root_causes", []),
            warning_signs_to_watch=data.get("warning_signs_to_watch", []),
            recommended_mitigations=data.get("recommended_mitigations", []),
            overall_risk_level=data.get("overall_risk_level", "Medium")
        )

    except Exception as e:
        print(f"Analyze failed: {e}")
        # Return fallback on error
        return AnalyzeResponse(
            project_description=request.project_description,
            risk_summary=f"Analysis failed due to error: {e}",
            top_analogous_failures=top_failures[:4],
            most_likely_root_causes=["Unknown"],
            warning_signs_to_watch=["Unknown"],
            recommended_mitigations=["Unknown"],
            overall_risk_level="High"
        )
