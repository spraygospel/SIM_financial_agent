# File: backend/mcp_servers/dummy_server.py

import sys
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="DummyServer", version="1.0.0")

@mcp.tool()
def echo(text: str) -> str:
    """Mengembalikan teks yang sama persis."""
    print(f"[DummyServer] Received echo request with text: {text}", file=sys.stderr)
    return text

if __name__ == "__main__":
    print(f"[{os.getpid()}] Starting DUMMY MCP Server...", file=sys.stderr)
    import os # butuh import os
    mcp.run()