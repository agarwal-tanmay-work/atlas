"""
Dan Luu Post-Mortem Ingestion Pipeline.

Parses all post-mortems from https://github.com/danluu/post-mortems,
fetches the content for each URL, uses Gemini to extract structured failure data,
and stores everything in PostgreSQL with pgvector embeddings.
"""

import sys
import os
import re
import time
import hashlib
import asyncio

import httpx
from bs4 import BeautifulSoup

# Add parent directory to path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import init_db, insert_failure, source_url_exists
from embeddings import embed_failure
from llm_extractor import extract_failure_from_text

# ----- Configuration -----
DANLUU_RAW_URL = "https://raw.githubusercontent.com/danluu/post-mortems/master/README.md"
MAX_CONCURRENT_FETCHES = 5
GEMINI_DELAY_SECONDS = 2  # Rate-limit delay between Gemini calls
FETCH_TIMEOUT = 20  # seconds per URL fetch
MAX_CONTENT_LENGTH = 6000  # characters of page content to send to Gemini


def parse_postmortem_entries(markdown_text: str) -> list[dict]:
    """
    Parse the Dan Luu README markdown and extract post-mortem entries.
    
    Each entry in the readme looks like:
    [Organization](url). Description text...
    
    Some entries start with a newline at the beginning, some are under section headers.
    We want the FIRST link in each entry paragraph along with its description.
    """
    entries = []
    seen_urls = set()

    # Section headers we want to STOP at (these contain meta-links, not post-mortems)
    stop_sections = [
        "## Other lists of postmortems",
        "## Analysis",
        "## Contributors",
    ]

    # Find where to stop parsing
    stop_index = len(markdown_text)
    for section in stop_sections:
        idx = markdown_text.find(section)
        if idx != -1 and idx < stop_index:
            stop_index = idx

    content = markdown_text[:stop_index]

    # Split by double newlines to get paragraph blocks
    blocks = re.split(r'\n\n+', content)

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        # Skip section headers
        if block.startswith("#"):
            continue
        if block.startswith("-") and "**[" in block:
            # Table of contents line
            continue

        # Find the first markdown link pattern [text](url)
        link_match = re.search(r'\[([^\]]+)\]\((https?://[^\)]+)\)', block)
        if not link_match:
            continue

        org_name = link_match.group(1)
        url = link_match.group(2)

        # Skip if we've already seen this URL
        if url in seen_urls:
            continue
        seen_urls.add(url)

        # Get the description - everything after the first link's closing paren
        # and any subsequent text in the block
        desc_start = link_match.end()
        description = block[desc_start:].strip()
        # Clean up the description: remove leading dots/periods
        description = re.sub(r'^[\.\s]+', '', description)
        # Also remove any additional markdown links, just keep text
        description_clean = re.sub(r'\[([^\]]*)\]\([^\)]*\)', r'\1', description)

        entries.append({
            "organization": org_name,
            "url": url,
            "description": description_clean.strip(),
            "raw_block": block,
        })

    return entries


async def fetch_page_content(url: str, client: httpx.AsyncClient) -> str | None:
    """Fetch a URL and extract readable text content."""
    try:
        response = await client.get(url, follow_redirects=True, timeout=FETCH_TIMEOUT)
        response.raise_for_status()

        content_type = response.headers.get("content-type", "")
        if "text/html" not in content_type and "text/plain" not in content_type:
            return None

        if "text/plain" in content_type:
            return response.text[:MAX_CONTENT_LENGTH]

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove script/style elements
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        # Try to find main content area
        main = soup.find("main") or soup.find("article") or soup.find("div", class_="post") or soup.find("body")
        if main:
            text = main.get_text(separator="\n", strip=True)
        else:
            text = soup.get_text(separator="\n", strip=True)

        # Clean up whitespace
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        text = "\n".join(lines)

        return text[:MAX_CONTENT_LENGTH] if text else None

    except Exception as e:
        print(f"  [!] Failed to fetch {url}: {e}")
        return None


async def fetch_all_pages(entries: list[dict]) -> dict[str, str]:
    """Fetch content for all URLs concurrently with a semaphore."""
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_FETCHES)
    results = {}

    async def fetch_one(entry: dict):
        url = entry["url"]
        async with semaphore:
            content = await fetch_page_content(url, client)
            if content:
                results[url] = content
            else:
                # Fall back to the markdown description
                if entry.get("description"):
                    results[url] = f"Organization: {entry['organization']}. {entry['description']}"

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; AtlasBot/1.0; +https://github.com/atlas-failures)",
        "Accept": "text/html,application/xhtml+xml,text/plain",
    }

    async with httpx.AsyncClient(headers=headers, follow_redirects=True) as client:
        tasks = [fetch_one(entry) for entry in entries]
        await asyncio.gather(*tasks, return_exceptions=True)

    return results


def run():
    print("=" * 60)
    print("  ATLAS - Dan Luu Post-Mortem Ingestion Pipeline")
    print("=" * 60)

    # 1. Initialize database
    print("\n[1/5] Initializing database...")
    init_db()

    # 2. Fetch & parse the Dan Luu README
    print("[2/5] Fetching Dan Luu post-mortems list...")
    import httpx as httpx_sync
    resp = httpx_sync.get(DANLUU_RAW_URL, timeout=30)
    resp.raise_for_status()
    markdown_text = resp.text

    entries = parse_postmortem_entries(markdown_text)
    print(f"  Found {len(entries)} post-mortem entries")

    # 3. Filter out already-ingested entries
    new_entries = []
    for entry in entries:
        if not source_url_exists(entry["url"]):
            new_entries.append(entry)
        else:
            print(f"  [+] Already ingested: {entry['organization']}")

    print(f"  {len(new_entries)} new entries to ingest")

    if not new_entries:
        print("\n[OK] All Dan Luu post-mortems are already ingested!")
        return

    # 4. Fetch web content for all new entries
    print(f"\n[3/5] Fetching web content for {len(new_entries)} URLs...")
    page_contents = asyncio.run(fetch_all_pages(new_entries))
    print(f"  Successfully fetched content for {len(page_contents)} URLs")

    # 5. Process each entry through Gemini
    print(f"\n[4/5] Extracting structured failure data via Gemini...")
    success_count = 0
    fail_count = 0

    for i, entry in enumerate(new_entries):
        url = entry["url"]
        org = entry["organization"]

        content = page_contents.get(url)
        if not content:
            print(f"  [{i+1}/{len(new_entries)}] [x] No content for {org} - skipping")
            fail_count += 1
            continue

        # Build a rich context for Gemini including the Dan Luu description
        analysis_text = f"Organization: {org}\nSource: {url}\n\n"
        if entry.get("description"):
            analysis_text += f"Summary from Dan Luu's post-mortem list:\n{entry['description']}\n\n"
        analysis_text += f"Full post-mortem content:\n{content}"

        print(f"  [{i+1}/{len(new_entries)}] Processing: {org}...", end=" ", flush=True)

        try:
            record = extract_failure_from_text(analysis_text, source_url=url)
        except Exception as e:
            print(f"[x] Gemini error: {e}")
            fail_count += 1
            time.sleep(GEMINI_DELAY_SECONDS)
            continue

        if record is None:
            print("[x] Extraction returned None")
            fail_count += 1
            time.sleep(GEMINI_DELAY_SECONDS)
            continue

        # Generate embedding
        try:
            embedding = embed_failure(record)
        except Exception as e:
            print(f"[x] Embedding error: {e}")
            fail_count += 1
            time.sleep(GEMINI_DELAY_SECONDS)
            continue

        # Store in PostgreSQL
        try:
            insert_failure(record, embedding)
            success_count += 1
            print(f"[+] {record.title}")
        except Exception as e:
            print(f"[x] DB insert error: {e}")
            fail_count += 1

        # Rate limit
        time.sleep(GEMINI_DELAY_SECONDS)

    # 6. Summary
    print(f"\n[5/5] Relationship mapping...")
    _run_relationship_engine()

    print("\n" + "=" * 60)
    print(f"  INGESTION COMPLETE")
    print(f"  [+] Successfully ingested: {success_count}")
    print(f"  [x] Failed: {fail_count}")
    print(f"  Total in database: ", end="")

    from database import count_failures
    print(f"{count_failures()}")
    print("=" * 60)


def _run_relationship_engine():
    """Map related failures using embedding similarity."""
    from database import get_all_failures, search_by_embedding, update_related_failures

    all_failures = get_all_failures(limit=500)
    for i, failure in enumerate(all_failures):
        embedding = embed_failure(failure)
        results = search_by_embedding(embedding, n_results=6)
        related_ids = [r["id"] for r in results if r["id"] != failure.id][:5]
        update_related_failures(failure.id, related_ids)

    print(f"  Mapped relationships for {len(all_failures)} failures")


if __name__ == "__main__":
    run()
