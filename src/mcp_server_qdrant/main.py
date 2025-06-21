import argparse
import os


def main():
    """
    Main entry point for the mcp-server-qdrant script defined
    in pyproject.toml. It runs the MCP server with a specific transport
    protocol.
    """

    # Parse the command-line arguments to determine the transport protocol.
    parser = argparse.ArgumentParser(description="mcp-server-qdrant")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse", "streamable-http"],
        default="stdio",
    )
    parser.add_argument(
        "--host",
        default=None,
        help="Host to bind the server to (overrides FASTMCP_HOST)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=None,
        help="Port to bind the server to (overrides FASTMCP_PORT)",
    )
    args = parser.parse_args()

    # Set environment variables if command line arguments are provided
    if args.host:
        os.environ["FASTMCP_HOST"] = args.host
    elif not os.environ.get("FASTMCP_HOST"):
        # Ensure we default to 0.0.0.0 for Railway deployment
        os.environ["FASTMCP_HOST"] = "0.0.0.0"
    
    if args.port:
        os.environ["FASTMCP_PORT"] = str(args.port)
    elif not os.environ.get("FASTMCP_PORT"):
        # Default port
        os.environ["FASTMCP_PORT"] = "8000"

    # Import is done here to make sure environment variables are loaded
    # only after we make the changes.
    from mcp_server_qdrant.server import mcp

    mcp.run(transport=args.transport)
