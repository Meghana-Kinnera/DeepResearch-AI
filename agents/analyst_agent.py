from config import get_llm_model
from typing import List, Dict

ANALYST_PROMPT = """You are a Lead Fact-Checker and Data Analyst.
Your goal is to evaluate raw web search results gathered for a specific sub-query and extract key verified facts, statistics, insights, and citations.

Sub-Query: "{query}"

Raw Search Results & Web Content:
{raw_content}

Instructions:
1. Extract key facts, data points, statistics, and insights directly relevant to the query.
2. Remove ads, promotional filler, repetitive statements, or noise.
3. Keep track of source URLs so they can be cited in the report.
4. Output structured markdown bullet points summarizing the verified findings for this query.
"""

def analyze_search_results(
    search_data: List[Dict], 
    model_name: str = "gemini-flash-latest", 
    api_key: str = None
) -> List[Dict[str, str]]:
    """
    Analyzes gathered search results for each query and produces extracted facts with source URLs.
    """
    model = get_llm_model(model_name, api_key)
    analyzed_insights = []
    
    for item in search_data:
        query = item.get("query", "")
        results = item.get("results", [])
        
        # Build raw content text for prompt
        content_blocks = []
        source_urls = []
        
        for r in results:
            url = r.get("url", "")
            title = r.get("title", "")
            text = r.get("content", "") or r.get("snippet", "")
            if url:
                source_urls.append({"title": title, "url": url})
            content_blocks.append(f"Source Title: {title}\nURL: {url}\nContent Snippet:\n{text}\n---")
            
        raw_content = "\n".join(content_blocks)
        
        if not raw_content.strip():
            continue
            
        prompt = ANALYST_PROMPT.format(query=query, raw_content=raw_content[:6000])
        
        try:
            response = model.generate_content(prompt)
            findings = response.text.strip()
        except Exception as e:
            findings = f"Failed to synthesize insights for '{query}': {e}"
            
        analyzed_insights.append({
            "query": query,
            "findings": findings,
            "sources": source_urls
        })
        
    return analyzed_insights
