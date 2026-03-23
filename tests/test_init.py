import pytest
import anyio
from crawl4ai_mcp.__init__ import crawl_tool, list_tools, app

@pytest.mark.anyio
async def test_list_tools():
    tools = await list_tools()
    assert len(tools) == 1
    assert tools[0].name == "crawl"

def test_app_exists():
    assert app.name == "mcp-web-crawler"
