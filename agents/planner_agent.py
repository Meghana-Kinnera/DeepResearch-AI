import json
from config import get_llm_model
from typing import List

PLANNER_PROMPT = """You are a Lead AI Research Planner.
Your task is to take a research topic provided by the user and break it down into exactly {num_queries} short, focused, highly effective web search queries.

Research Topic: "{topic}"

CRITICAL RULES for Search Queries:
1. Keep each query SHORT (3 to 6 words max). Do NOT concatenate long strings of jargon into one giant query.
2. Ensure queries cover: recent trends, technical architecture, security/challenges, and future outlook.

Output Format: Return ONLY a valid JSON array of strings containing the queries.
Example format for 3 queries:
["query 1", "query 2", "query 3"]
Do NOT wrap in markdown codeblocks if possible, or use standard ```json block. Do NOT add extra conversational text.
"""

def generate_research_plan(topic: str, num_queries: int = 4, model_name: str = "gemini-flash-latest", api_key: str = None) -> List[str]:
    """Generates short, focused search sub-queries for a given research topic."""
    model = get_llm_model(model_name, api_key)
    prompt = PLANNER_PROMPT.format(topic=topic, num_queries=num_queries)
    
    response = model.generate_content(prompt)
    raw_text = response.text.strip()
    
    if raw_text.startswith("```"):
        lines = raw_text.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        raw_text = "\n".join(lines).strip()
        
    try:
        queries = json.loads(raw_text)
        if isinstance(queries, list) and len(queries) > 0:
            return [str(q).strip() for q in queries[:num_queries]]
    except Exception as e:
        print(f"[Planner Warning] Could not parse JSON array directly: {e}")
    
    words = topic.split()[:4]
    short_topic = " ".join(words)
    fallback_queries = [
        f"{short_topic} trends 2026",
        f"{short_topic} architecture developer productivity",
        f"{short_topic} security risks code quality",
        f"future of software development {short_topic}"
    ]
    return fallback_queries[:num_queries]
