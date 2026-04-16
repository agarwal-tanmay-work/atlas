"""
GitHub post-mortem fetcher.

Fetches post-mortem entries from danluu/post-mortems and similar repositories.
This module is optional — the seed_data.py provides all necessary data for the demo.
"""

import httpx
from bs4 import BeautifulSoup


async def fetch_github_postmortems(limit: int = 20) -> list[dict]:
    """
    Fetches post-mortem links from the danluu/post-mortems repository.
    Returns a list of dicts with 'title', 'url', and 'raw_text' fields.
    
    Note: This is supplementary to seed_data.py. The seed data provides
    60+ hardcoded failures for offline demo capability.
    """
    url = "https://raw.githubusercontent.com/danluu/post-mortems/master/README.md"
    
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(url)
            response.raise_for_status()
            
        content = response.text
        lines = content.split("\n")
        
        entries = []
        for line in lines:
            if line.startswith("- [") or line.startswith("* ["):
                # Extract markdown link
                try:
                    title_start = line.index("[") + 1
                    title_end = line.index("]")
                    url_start = line.index("(") + 1
                    url_end = line.index(")")
                    
                    title = line[title_start:title_end]
                    link = line[url_start:url_end]
                    
                    entries.append({
                        "title": title,
                        "url": link,
                        "raw_text": "",  # Would need to fetch each URL
                    })
                except ValueError:
                    continue
                    
            if len(entries) >= limit:
                break
                
        return entries
        
    except Exception as e:
        print(f"Failed to fetch GitHub post-mortems: {e}")
        return []
