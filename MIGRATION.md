# Migration Guide: TypeScript to Python (Databricks)

This document explains the differences between the original TypeScript implementation and the new Python/Databricks implementation.

## Overview

This repository now contains **two implementations** of the MCP Sequential Thinking Tools:

1. **Original TypeScript/Node.js** - For traditional MCP clients (Claude Desktop, Cline)
2. **New Python/FastAPI** - For Databricks Apps deployment

## Key Differences

### Architecture

| Feature | TypeScript | Python/Databricks |
|---------|-----------|-------------------|
| Runtime | Node.js | Python 3.11+ |
| Framework | tmcp | FastMCP |
| Transport | stdio | Streamable HTTP |
| Deployment | npm/npx | Databricks Apps |
| Schema | Valibot | Pydantic |
| Server | Direct MCP | FastAPI + MCP |

### File Structure

#### TypeScript Implementation
```
src/
├── index.ts         # Main entry point
├── schema.ts        # Valibot schemas
└── types.ts         # TypeScript interfaces
package.json         # Node dependencies
tsconfig.json        # TypeScript config
```

#### Python Implementation
```
src/mcp_sequentialthinking_databricks/
├── __init__.py      # Package init
├── app.py           # FastAPI application
├── main.py          # Entry point
├── server.py        # Core logic
├── schema.py        # Tool definitions
├── types.py         # Pydantic models
└── static/
    └── index.html   # Web interface
pyproject.toml       # Python dependencies
databricks.yml       # Databricks config
app.yaml             # App command config
hooks/
└── apps_build.py    # Build hook
```

## Feature Parity

Both implementations provide the same core functionality:

✅ Sequential thinking with thought tracking
✅ Tool recommendations with confidence scores
✅ Branch and revision support
✅ Memory management with history limits
✅ Configurable via environment variables

### Additional Features in Python Version

- 🌐 Web interface at root URL
- 🏥 Health check endpoint (`/health`)
- 📊 Better logging and monitoring
- 🚀 Production-ready deployment on Databricks
- 🔐 Bearer token authentication support

## When to Use Which Version

### Use TypeScript Version When:
- Running MCP client locally (Claude Desktop, Cline)
- Using stdio transport
- Need quick local development
- Prefer Node.js ecosystem

### Use Python Version When:
- Deploying to Databricks
- Need web-based access
- Want production deployment
- Prefer Python ecosystem
- Need REST API access
- Want monitoring dashboards

## Running Both Versions

You can use both versions in the same repository:

### TypeScript (Local)
```bash
# Install and run
pnpm install
pnpm build
pnpm start
```

### Python (Databricks)
```bash
# Install and run
uv sync
uv run mcp-sequentialthinking-databricks
```

## Configuration Comparison

### TypeScript (stdio)
```json
{
  "mcpServers": {
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "mcp-sequentialthinking-tools"],
      "env": {
        "MAX_HISTORY_SIZE": "1000"
      }
    }
  }
}
```

### Python (HTTP)
```json
{
  "mcpServers": {
    "sequential-thinking": {
      "transport": "streamable-http",
      "url": "https://your-app.databricks.com/mcp/",
      "auth": {
        "type": "bearer",
        "token": "your-token"
      }
    }
  }
}
```

## API Compatibility

Both versions expose the same MCP tool:

**Tool Name:** `sequentialthinking_tools`

**Parameters:** (Identical in both versions)
- `available_mcp_tools`: Array of tool names
- `thought`: Current thinking step
- `next_thought_needed`: Boolean
- `thought_number`: Integer
- `total_thoughts`: Integer
- ... (all other parameters match)

**Response Format:** (Identical structure)

## Migration Path

### From TypeScript to Python

1. **Keep TypeScript for local development:**
   ```bash
   pnpm install && pnpm build
   ```

2. **Add Python for Databricks:**
   ```bash
   uv sync
   uv build --wheel
   databricks bundle deploy
   ```

3. **Update MCP clients:**
   - Local clients → Keep using TypeScript (stdio)
   - Remote/web clients → Use Python (HTTP)

### Development Workflow

```bash
# Local testing (TypeScript)
pnpm dev

# Local testing (Python)
uv run mcp-sequentialthinking-databricks

# Deploy to Databricks (Python)
uv build --wheel && databricks bundle deploy
```

## Code Translation Examples

### Schema Definition

**TypeScript (Valibot):**
```typescript
export const ToolRecommendationSchema = v.object({
  tool_name: v.pipe(v.string(), v.description('...')),
  confidence: v.pipe(v.number(), v.minValue(0), v.maxValue(1)),
  // ...
});
```

**Python (Pydantic):**
```python
class ToolRecommendation(BaseModel):
    tool_name: str = Field(description="...")
    confidence: float = Field(ge=0, le=1)
    # ...
```

### Tool Registration

**TypeScript:**
```typescript
server.tool(
  {
    name: 'sequentialthinking_tools',
    description: TOOL_DESCRIPTION,
    schema: SequentialThinkingSchema,
  },
  async (input) => {
    return thinkingServer.processThought(input);
  }
);
```

**Python:**
```python
@mcp.tool()
def sequentialthinking_tools(
    available_mcp_tools: list[str],
    thought: str,
    # ... parameters
) -> dict:
    thought_data = ThoughtData(...)
    return thinking_server.process_thought(thought_data)
```

## Performance Considerations

### TypeScript
- ⚡ Fast startup time
- 💾 Lower memory footprint
- 🔌 Direct stdio communication
- 📦 Smaller package size

### Python
- 🌐 Better for web/HTTP
- 📊 Rich monitoring capabilities
- 🔄 Handles concurrent requests
- 🚀 Scales on Databricks

## Support Matrix

| Feature | TypeScript | Python |
|---------|-----------|--------|
| Claude Desktop | ✅ | ❌* |
| Cline | ✅ | ❌* |
| Web MCP Clients | ❌ | ✅ |
| Databricks | ❌ | ✅ |
| CI/CD | ⚠️ | ✅ |
| Docker | ⚠️ | ✅ |

*Can work with HTTP transport adapter

## Future Plans

- Both implementations will be maintained
- Feature parity maintained between versions
- TypeScript for local/desktop use
- Python for cloud/production use
- Consider unified documentation

## Getting Help

- TypeScript issues → Check `package.json` and `src/` files
- Python issues → Check `pyproject.toml` and `src/mcp_sequentialthinking_databricks/`
- Databricks deployment → See [QUICKSTART.md](QUICKSTART.md)
- General usage → See [README.md](README.md)

## Conclusion

**Both versions are first-class implementations.** Choose based on your deployment target:

- 🖥️ **Desktop/Local** → TypeScript
- ☁️ **Cloud/Databricks** → Python

You can even use both in different contexts!
