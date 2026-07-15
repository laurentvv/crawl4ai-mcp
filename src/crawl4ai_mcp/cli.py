import os
import sys
import traceback
import click
import anyio
import uvicorn
from starlette.applications import Starlette
from starlette.routing import Mount, Route
from mcp.server.sse import SseServerTransport
from mcp.server.stdio import stdio_server
from mcp.server.lowlevel import Server

from .server import app

def run_sse_server(app: Server, port: int):
    sse = SseServerTransport("/messages/")

    async def handle_sse(request):
        async with sse.connect_sse(
            request.scope, request.receive, request.send
        ) as streams:
            await app.run(
                streams[0], streams[1], app.create_initialization_options()
            )

    starlette_app = Starlette(
        debug=os.getenv("CRAWL4AI_MCP_DEBUG", "False").lower() == "true",
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/messages/", app=sse.handle_post_message),
        ],
    )

    uvicorn.run(starlette_app, host="127.0.0.1", port=port)

def run_stdio_server(app: Server):
    async def arun():
        async with stdio_server() as streams:
            await app.run(
                streams[0], streams[1], app.create_initialization_options()
            )

    anyio.run(arun)

@click.command()
@click.option("--port", default=8000, help="Port to listen on for SSE")
@click.option(
    "--transport",
    type=click.Choice(["stdio", "sse"]),
    default="stdio",
    help="Transport type",
)
def main(port: int, transport: str) -> int:
    if transport == "sse":
        run_sse_server(app, port)
    else:
        run_stdio_server(app)
    return 0

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Main error: {e}", file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        sys.exit(1)
