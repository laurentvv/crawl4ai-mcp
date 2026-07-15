import os

TEST_DIR = 'tests'

MOCK_MAPPINGS = {
    'crawl4ai_mcp.datetime': 'crawl4ai_mcp.utils.datetime',
    'crawl4ai_mcp.anyio.Path': 'crawl4ai_mcp.crawler.anyio.Path',
    'crawl4ai_mcp.AsyncWebCrawler': 'crawl4ai_mcp.crawler.AsyncWebCrawler',
    'crawl4ai_mcp.results_to_markdown': 'crawl4ai_mcp.crawler.results_to_markdown',
    'crawl4ai_mcp.Starlette': 'crawl4ai_mcp.cli.Starlette',
    'crawl4ai_mcp.uvicorn': 'crawl4ai_mcp.cli.uvicorn',
    'crawl4ai_mcp.SseServerTransport': 'crawl4ai_mcp.cli.SseServerTransport',
}

for f in os.listdir(TEST_DIR):
    if not f.endswith('.py'):
        continue
    filepath = os.path.join(TEST_DIR, f)
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
    
    for old, new in MOCK_MAPPINGS.items():
        content = content.replace(f'"{old}"', f'"{new}"')
        content = content.replace(f"'{old}'", f"'{new}'")
        
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(content)

print("Patching complete")
