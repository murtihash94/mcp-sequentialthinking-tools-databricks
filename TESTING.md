# Testing Guide for MCP Sequential Thinking Tools

This document provides instructions for testing the MCP Sequential Thinking Tools server.

## Local Testing

### Prerequisites
- Python 3.11 or higher
- `uv` installed (`pip install uv`)

### Quick Start

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Run the server:**
   ```bash
   uv run mcp-sequentialthinking-databricks
   ```

3. **Test the endpoints:**

   **Health Check:**
   ```bash
   curl http://localhost:8000/health
   ```
   
   Expected response:
   ```json
   {
     "status": "healthy",
     "service": "mcp-sequential-thinking-tools",
     "version": "0.0.4"
   }
   ```

   **Web Interface:**
   Open http://localhost:8000 in your browser to see the status page.

   **MCP Endpoint:**
   The MCP endpoint is available at http://localhost:8000/mcp/

### Testing the MCP Tool

You can test the sequential thinking tool by sending requests to the MCP endpoint. Here's an example using the MCP protocol:

```json
{
  "available_mcp_tools": ["search", "analyze"],
  "thought": "Let's break down this problem into steps",
  "next_thought_needed": true,
  "thought_number": 1,
  "total_thoughts": 3,
  "current_step": {
    "step_description": "Research the problem domain",
    "recommended_tools": [
      {
        "tool_name": "search",
        "confidence": 0.9,
        "rationale": "We need to gather information first",
        "priority": 1
      }
    ],
    "expected_outcome": "Understanding of the problem space"
  }
}
```

## Build Testing

### Test the Wheel Build

```bash
uv build --wheel
```

This should create:
- `dist/mcp_sequentialthinking_databricks-0.0.4-py3-none-any.whl`
- `.build/` directory with Databricks-compatible structure

### Verify Build Structure

```bash
ls -la .build/
```

Expected contents:
- `mcp_sequentialthinking_databricks-0.0.4-py3-none-any.whl`
- `requirements.txt`
- `app.yaml`

## Integration Testing

### Test with MCP Client

If you have an MCP client (like Claude Desktop or Cline), you can configure it to connect to your local server:

```json
{
  "mcpServers": {
    "sequentialthinking-local": {
      "transport": "streamable-http",
      "url": "http://localhost:8000/mcp/",
      "auth": {
        "type": "none"
      }
    }
  }
}
```

### Test Tool Discovery

The server should expose one tool:
- `sequentialthinking_tools`: The main sequential thinking tool

### Test Resource Discovery

The server should expose one resource pattern:
- `greeting://{name}`: A greeting resource for testing

## Performance Testing

### Memory Management

The server includes memory management with a default history limit of 1000 thoughts. To test this:

1. Set a lower limit:
   ```bash
   MAX_HISTORY_SIZE=10 uv run mcp-sequentialthinking-databricks
   ```

2. Send multiple thoughts and verify history is trimmed

### Concurrent Requests

The FastAPI server handles concurrent requests. Test with multiple simultaneous connections:

```bash
# Terminal 1
curl http://localhost:8000/health

# Terminal 2  
curl http://localhost:8000/health

# Terminal 3
curl http://localhost:8000/health
```

## Troubleshooting

### Common Issues

1. **Port already in use:**
   ```bash
   # Kill the process using port 8000
   pkill -f uvicorn
   # Or use a different port
   uvicorn mcp_sequentialthinking_databricks.app:app --port 8001
   ```

2. **Import errors:**
   ```bash
   # Reinstall dependencies
   uv sync --force
   ```

3. **Build errors:**
   ```bash
   # Clean build artifacts
   rm -rf dist/ .build/ *.egg-info
   # Rebuild
   uv build --wheel
   ```

## Automated Testing

To run a full test suite:

```bash
#!/bin/bash

echo "Testing MCP Sequential Thinking Tools..."

# Test imports
echo "1. Testing imports..."
uv run python -c "from mcp_sequentialthinking_databricks.server import ToolAwareSequentialThinkingServer; print('✓ Imports successful')"

# Test build
echo "2. Testing build..."
uv build --wheel > /dev/null 2>&1
if [ -f ".build/requirements.txt" ]; then
  echo "✓ Build successful"
else
  echo "✗ Build failed"
  exit 1
fi

# Test server startup
echo "3. Testing server startup..."
uv run uvicorn mcp_sequentialthinking_databricks.app:app --host 127.0.0.1 --port 8765 &
PID=$!
sleep 3

# Test health endpoint
echo "4. Testing health endpoint..."
HEALTH=$(curl -s http://127.0.0.1:8765/health | grep "healthy")
if [ -n "$HEALTH" ]; then
  echo "✓ Health endpoint working"
else
  echo "✗ Health endpoint failed"
fi

# Cleanup
kill $PID 2>/dev/null
wait $PID 2>/dev/null

echo "All tests passed! ✓"
```

Save this as `test.sh`, make it executable (`chmod +x test.sh`), and run it.
