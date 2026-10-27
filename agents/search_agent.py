from tools.search_tool import execute_web_search, scrape_page_content
from typing import List, Dict, Callable

def run_search_workflow(
    queries: List[str], 
    status_callback: Callable[[str], None] = None
) -> List[Dict]:
    """
    Executes search queries, retrieves page content, and aggregates search results.
    Calls status_callback with progress updates for UI.
    """
    all_search_data = []
    
    for idx, query in enumerate(queries, 1):
        if status_callback:
            status_callback(f"🌐 Search Agent executing query {idx}/{len(queries)}: '{query}'")
            
        search_results = execute_web_search(query, max_results=3)
        
        query_data = {
            "query": query,
            "results": []
        }
        
        for item in search_results:
            title = item.get("title", "")
            url = item.get("url", "")
            snippet = item.get("snippet", "")
            
            # Scrape deep content if snippet is short
            scraped_content = ""
            if url:
                if status_callback:
                    status_callback(f"📄 Fetching page content from: {url[:50]}...")
                scraped_content = scrape_page_content(url, max_chars=2000)
            
            combined_text = scraped_content if scraped_content else snippet
            
            query_data["results"].append({
                "title": title,
                "url": url,
                "snippet": snippet,
                "content": combined_text
            })
            
        all_search_data.append(query_data)
        
    return all_search_data
