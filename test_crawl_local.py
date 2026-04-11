import pytest
import asyncio
from src.crawl4ai_mcp import crawl_tool

@pytest.mark.anyio
async def test_ansible_docs():
    print("Starting crawl of Ansible docs with advanced options...")
    args = {
        "url": "https://docs.ansible.com",
        "magic": True,
        "delay_before_return_html": 2.0,
        "verbose": False
    }

    result = await crawl_tool("crawl", args)
    print("Crawl Tool Result:")
    for content in result:
        print(f"Content Type: {content.type}")
        print(content.text[:1000] + "...\n" if len(content.text) > 1000 else content.text)

if __name__ == "__main__":
    asyncio.run(test_ansible_docs())
