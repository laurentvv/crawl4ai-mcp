import asyncio
from crawl4ai_mcp import crawl_and_output_to_markdown

async def main():
    print("Testing crawl of docs.ansible.com")
    result = await crawl_and_output_to_markdown(
        start_url="https://docs.ansible.com",
        max_depth=1,
        include_external=False,
        verbose=True
    )
    print("Success?", "stats" in result and result.get("error") is None)

if __name__ == "__main__":
    asyncio.run(main())
