"""Main entry point for the MCP Sequential Thinking server."""

import uvicorn


def main():
    """Run the server."""
    uvicorn.run(
        "mcp_sequentialthinking_databricks.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    main()
