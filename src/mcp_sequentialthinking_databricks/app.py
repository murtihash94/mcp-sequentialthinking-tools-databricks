"""FastAPI application for MCP Sequential Thinking server on Databricks."""

import logging
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from fastapi import FastAPI
from fastapi.responses import FileResponse
from .server import ToolAwareSequentialThinkingServer
from .types import ThoughtData

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

STATIC_DIR = Path(__file__).parent / "static"

# Create an MCP server
mcp = FastMCP("MCP Sequential Thinking Tools on Databricks Apps")

# Initialize the sequential thinking server
thinking_server = ToolAwareSequentialThinkingServer()


@mcp.tool()
def sequentialthinking_tools(
    available_mcp_tools: list[str],
    thought: str,
    next_thought_needed: bool,
    thought_number: int,
    total_thoughts: int,
    is_revision: bool | None = None,
    revises_thought: int | None = None,
    branch_from_thought: int | None = None,
    branch_id: str | None = None,
    needs_more_thoughts: bool | None = None,
    current_step: dict | None = None,
    previous_steps: list[dict] | None = None,
    remaining_steps: list[str] | None = None,
) -> dict:
    """
    A detailed tool for dynamic and reflective problem-solving through thoughts.
    
    This tool helps analyze problems through a flexible thinking process that can adapt
    and evolve. Each thought can build on, question, or revise previous insights as
    understanding deepens.
    
    Args:
        available_mcp_tools: Array of MCP tool names available for use
        thought: Your current thinking step
        next_thought_needed: Whether another thought step is needed
        thought_number: Current thought number
        total_thoughts: Estimated total thoughts needed
        is_revision: Whether this revises previous thinking
        revises_thought: Which thought is being reconsidered
        branch_from_thought: Branching point thought number
        branch_id: Branch identifier
        needs_more_thoughts: If more thoughts are needed
        current_step: Current step recommendation
        previous_steps: Steps already recommended
        remaining_steps: High-level descriptions of upcoming steps
    
    Returns:
        Dict containing the processing result
    """
    try:
        # Create ThoughtData object
        thought_data = ThoughtData(
            available_mcp_tools=available_mcp_tools,
            thought=thought,
            next_thought_needed=next_thought_needed,
            thought_number=thought_number,
            total_thoughts=total_thoughts,
            is_revision=is_revision,
            revises_thought=revises_thought,
            branch_from_thought=branch_from_thought,
            branch_id=branch_id,
            needs_more_thoughts=needs_more_thoughts,
            current_step=current_step,
            previous_steps=previous_steps,
            remaining_steps=remaining_steps,
        )
        
        # Process the thought
        result = thinking_server.process_thought(thought_data)
        logger.info(f"Processed thought {thought_number}/{total_thoughts}")
        return result
    except Exception as e:
        logger.error(f"Error in sequentialthinking_tools: {e}", exc_info=True)
        return {
            "error": str(e),
            "status": "failed"
        }


@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting."""
    return f"Hello, {name}! Welcome to MCP Sequential Thinking Tools on Databricks."


# Create the MCP app with streamable HTTP
mcp_app = mcp.streamable_http_app()

# Create the main FastAPI app
app = FastAPI(
    title="MCP Sequential Thinking Tools",
    description="Sequential thinking server with tool recommendations for Databricks",
    version="0.0.4",
    lifespan=lambda _: mcp.session_manager.run(),
)


@app.get("/", include_in_schema=False)
async def serve_index():
    """Serve the index page."""
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "mcp-sequential-thinking-tools",
        "version": "0.0.4"
    }


# Mount the MCP app
app.mount("/", mcp_app)
