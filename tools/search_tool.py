import requests
from bs4 import BeautifulSoup
try:
    from ddgs import DDGS
except ImportError:
    from duckduckgo_search import DDGS
from typing import List, Dict

IGNORED_DOMAINS = ["youtube.com", "zhihu.com", "dictionary.cambridge.org", "wikipedia.org/wiki/Future"]

def execute_web_search(query: str, max_results: int = 4) -> List[Dict[str, str]]:
    """
    Executes a web search using DuckDuckGo.
    Filters out noisy/irrelevant domains.
    """
    results = []
    try:
        with DDGS() as ddgs:
            ddg_gen = ddgs.text(query, max_results=max_results + 3)
            for r in ddg_gen:
                url = r.get("href", r.get("link", ""))
                title = r.get("title", "")
                snippet = r.get("body", r.get("snippet", ""))
                
                # Filter out obvious noisy domains
                if any(domain in url.lower() for domain in IGNORED_DOMAINS):
                    continue
                    
                results.append({
                    "title": title,
                    "url": url,
                    "snippet": snippet
                })
                if len(results) >= max_results:
                    break
    except Exception as e:
        print(f"[SearchTool Error] Query '{query}' search failed: {e}")
    return results

def scrape_page_content(url: str, max_chars: int = 2500) -> str:
    """
    Fetches web page content and extracts readable text paragraphs.
    Truncates content to max_chars to avoid excessive token consumption.
    """
    if not url or not url.startswith("http"):
        return ""
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=6)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for script in soup(["script", "style", "nav", "footer", "header", "form"]):
                script.extract()
            
            paragraphs = soup.find_all(['p', 'h1', 'h2', 'h3', 'article'])
            text_blocks = [p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 30]
            
            full_text = "\n".join(text_blocks)
            return full_text[:max_chars]
    except Exception as e:
        print(f"[Scraper Warning] Failed to scrape {url}: {e}")
    
    return ""
