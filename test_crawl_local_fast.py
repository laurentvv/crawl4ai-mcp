import pytest
import asyncio
from src.crawl4ai_mcp import crawl_tool

@pytest.mark.anyio
async def test_ansible_docs():
    print("Starting crawl of Ansible docs with basic extraction...")
    args = {
        "url": "https://docs.ansible.com",
        "css_selector": "h1, p.lead",
        "magic": True,
        "verbose": True
    }

    result = await crawl_tool("crawl", args)
    print("\n--- RESULTS ---")
    for content in result:
        print(content.text[:1000] + "...\n" if len(content.text) > 1000 else content.text)

if __name__ == "__main__":
    asyncio.run(test_ansible_docs())
