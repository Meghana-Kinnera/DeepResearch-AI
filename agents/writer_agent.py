from config import get_llm_model
from typing import List, Dict

WRITER_PROMPT = """You are a Principal Technical Writer and Senior Industry Analyst.
Your mission is to write a comprehensive, highly detailed, publication-quality **Deep Research Report** based on the synthesized web research provided below.

Topic: "{topic}"

Synthesized Insights by Sub-Queries:
{insights_summary}

Compiled Sources & URLs:
{sources_summary}

Instructions for the Report:
1. Title: Create a compelling, executive-level title.
2. Executive Summary: Provide a 2-3 paragraph overview of the current state, technological shifts, and core conclusions.
3. Detailed Technical Analysis: Organize into 3-4 structured sections with clear markdown headings (##, ###). Synthesize deep insights on trends, architectures, workflows, developer productivity, code security, and enterprise adoption.
4. Challenges & Future Outlook: Detail technical debt, security risks, SWE-bench performance benchmarks, and projections for 2026+.
5. Conclusion: A clear summary wrap-up.
6. References & Citations: List the referenced source URLs as clickable markdown links.

Tone: Authoritative, analytical, well-structured, professional Markdown formatting.
Start directly with the markdown title (# Title).
"""

def generate_final_report(
    topic: str, 
    analyzed_insights: List[Dict], 
    model_name: str = "gemini-flash-latest", 
    api_key: str = None
) -> str:
    """
    Generates a full Markdown research report by assembling analyzed insights.
    """
    model = get_llm_model(model_name, api_key)
    
    insights_blocks = []
    all_sources = []
    
    for item in analyzed_insights:
        q = item.get("query", "")
        f = item.get("findings", "")
        insights_blocks.append(f"### Sub-Topic: {q}\n{f}\n")
        
        for s in item.get("sources", []):
            if s not in all_sources:
                all_sources.append(s)
                
    insights_summary = "\n".join(insights_blocks)
    
    sources_blocks = []
    for idx, s in enumerate(all_sources, 1):
        title = s.get("title", f"Source {idx}")
        url = s.get("url", "")
        if url:
            sources_blocks.append(f"- [{title}]({url})")
            
    sources_summary = "\n".join(sources_blocks) if sources_blocks else "No external source URLs recorded."
    
    prompt = WRITER_PROMPT.format(
        topic=topic,
        insights_summary=insights_summary[:12000],
        sources_summary=sources_summary[:3000]
    )
    
    try:
        response = model.generate_content(prompt)
        report_markdown = response.text.strip()
        return report_markdown
    except Exception as e:
        print(f"[Writer Agent Error] {e}")
        return f"# Deep Research Report: {topic}\n\n## Executive Summary\nAnalysis generated based on web retrieval.\n\n## Key Findings\n{insights_summary}\n\n## References\n{sources_summary}"
