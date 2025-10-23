# mcp-sequentialthinking-tools-databricks

An adaptation of the
[MCP Sequential Thinking Server](https://github.com/modelcontextprotocol/servers/blob/main/src/sequentialthinking/index.ts)
designed to run on **Databricks Apps**. This server helps
break down complex problems into manageable steps and provides
recommendations for which MCP tools would be most effective at each
stage.

<a href="https://glama.ai/mcp/servers/zl990kfusy">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/zl990kfusy/badge" />
</a>

A Model Context Protocol (MCP) server that combines sequential
thinking with intelligent tool suggestions. For each step in the
problem-solving process, it provides confidence-scored recommendations
for which tools to use, along with rationale for why each tool would
be appropriate.

**🎯 Now deployable on Databricks Apps!** This version has been converted to a Python-based FastAPI application that can be easily deployed to Databricks.

## 📚 Documentation

- **[Quick Start Guide](QUICKSTART.md)** - Get deployed to Databricks in 15 minutes
- **[Migration Guide](MIGRATION.md)** - Understand TypeScript vs Python implementations  
- **[Testing Guide](TESTING.md)** - Comprehensive testing documentation
- **[Full Documentation](#databricks-deployment)** - Detailed deployment instructions below

## 🖼️ Web Interface

Once deployed, the server provides a beautiful web interface:

![MCP Sequential Thinking Tools Web Interface](https://github.com/user-attachments/assets/b120c387-cf72-4af5-8b2c-943b8105dbf9)

The interface includes:
- 🎨 Modern, responsive design
- 📊 Real-time server status
- 🔗 MCP endpoint information
- 🏥 Health check endpoint
- ✨ Complete feature list
- 📝 Version and protocol information

## Features

- 🤔 Dynamic and reflective problem-solving through sequential
  thoughts
- 🔄 Flexible thinking process that adapts and evolves
- 🌳 Support for branching and revision of thoughts
- 🛠️ LLM-driven intelligent tool recommendations for each step
- 📊 Confidence scoring for tool suggestions
- 🔍 Detailed rationale for tool recommendations
- 📝 Step tracking with expected outcomes
- 🔄 Progress monitoring with previous and remaining steps
- 🎯 Alternative tool suggestions for each step
- 🧠 Memory management with configurable history limits
- 🗑️ Manual history cleanup capabilities

## How It Works

This server facilitates sequential thinking with MCP tool coordination. The LLM analyzes available tools and their descriptions to make intelligent recommendations, which are then tracked and organized by this server.

The workflow:
1. LLM provides available MCP tools to the sequential thinking server
2. LLM analyzes each thought step and recommends appropriate tools
3. Server tracks recommendations, maintains context, and manages memory
4. LLM executes recommended tools and continues the thinking process

Each recommendation includes:
- A confidence score (0-1) indicating how well the tool matches the need
- A clear rationale explaining why the tool would be helpful
- A priority level to suggest tool execution order
- Suggested input parameters for the tool
- Alternative tools that could also be used

The server works with any MCP tools available in your environment and automatically manages memory to prevent unbounded growth.

## Example Usage

Here's an example of how the server guides tool usage:

```json
{
	"thought": "Initial research step to understand what universal reactivity means in Svelte 5",
	"current_step": {
		"step_description": "Gather initial information about Svelte 5's universal reactivity",
		"expected_outcome": "Clear understanding of universal reactivity concept",
		"recommended_tools": [
			{
				"tool_name": "search_docs",
				"confidence": 0.9,
				"rationale": "Search Svelte documentation for official information",
				"priority": 1
			},
			{
				"tool_name": "tavily_search",
				"confidence": 0.8,
				"rationale": "Get additional context from reliable sources",
				"priority": 2
			}
		],
		"next_step_conditions": [
			"Verify information accuracy",
			"Look for implementation details"
		]
	},
	"thought_number": 1,
	"total_thoughts": 5,
	"next_thought_needed": true
}
```

The server tracks your progress and supports:

- Creating branches to explore different approaches
- Revising previous thoughts with new information
- Maintaining context across multiple steps
- Suggesting next steps based on current findings

## Configuration

This server can be run in two ways:
1. **Traditional MCP Client** (original TypeScript version - still supported)
2. **Databricks Apps** (new Python version - recommended for production)

### Traditional MCP Configuration

#### Cline Configuration

Add this to your Cline MCP settings:

```json
{
	"mcpServers": {
		"mcp-sequentialthinking-tools": {
			"command": "npx",
			"args": ["-y", "mcp-sequentialthinking-tools"],
			"env": {
				"MAX_HISTORY_SIZE": "1000"
			}
		}
	}
}
```

#### Claude Desktop with WSL Configuration

For WSL environments, add this to your Claude Desktop configuration:

```json
{
	"mcpServers": {
		"mcp-sequentialthinking-tools": {
			"command": "wsl.exe",
			"args": [
				"bash",
				"-c",
				"MAX_HISTORY_SIZE=1000 source ~/.nvm/nvm.sh && /home/username/.nvm/versions/node/v20.12.1/bin/npx mcp-sequentialthinking-tools"
			]
		}
	}
}
```

### Databricks Apps Configuration

See the [Databricks Deployment](#databricks-deployment) section below for detailed instructions on deploying to Databricks Apps.

## API

The server implements a single MCP tool with configurable parameters:

### sequentialthinking_tools

A tool for dynamic and reflective problem-solving through thoughts,
with intelligent tool recommendations.

Parameters:

- `available_mcp_tools` (array, required): Array of MCP tool names available for use (e.g., ["mcp-omnisearch", "mcp-turso-cloud"])
- `thought` (string, required): Your current thinking step
- `next_thought_needed` (boolean, required): Whether another thought
  step is needed
- `thought_number` (integer, required): Current thought number
- `total_thoughts` (integer, required): Estimated total thoughts
  needed
- `is_revision` (boolean, optional): Whether this revises previous
  thinking
- `revises_thought` (integer, optional): Which thought is being
  reconsidered
- `branch_from_thought` (integer, optional): Branching point thought
  number
- `branch_id` (string, optional): Branch identifier
- `needs_more_thoughts` (boolean, optional): If more thoughts are
  needed
- `current_step` (object, optional): Current step recommendation with:
  - `step_description`: What needs to be done
  - `recommended_tools`: Array of tool recommendations with confidence
    scores
  - `expected_outcome`: What to expect from this step
  - `next_step_conditions`: Conditions for next step
- `previous_steps` (array, optional): Steps already recommended
- `remaining_steps` (array, optional): High-level descriptions of
  upcoming steps

## Memory Management

The server includes built-in memory management to prevent unbounded growth:

- **History Limit**: Configurable maximum number of thoughts to retain (default: 1000)
- **Automatic Trimming**: History automatically trims when limit is exceeded
- **Manual Cleanup**: Server provides methods to clear history when needed

### Configuring History Size

You can configure the history size by setting the `MAX_HISTORY_SIZE` environment variable:

```json
{
  "mcpServers": {
    "mcp-sequentialthinking-tools": {
      "command": "npx",
      "args": ["-y", "mcp-sequentialthinking-tools"],
      "env": {
        "MAX_HISTORY_SIZE": "500"
      }
    }
  }
}
```

Or for local development:
```bash
MAX_HISTORY_SIZE=2000 npx mcp-sequentialthinking-tools
```

## Databricks Deployment

This MCP server has been converted to a Databricks App structure using Python and FastAPI. Follow these steps to deploy it on Databricks Apps.

### Prerequisites

- Databricks CLI installed and configured
- `uv` (Python package installer, faster alternative to pip)
- Python 3.11 or higher
- Access to a Databricks workspace

### Installation

#### Install Databricks CLI

```bash
# macOS/Linux
curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sh

# Or using pip
pip install databricks-cli
```

#### Install UV (Python package manager)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or using pip
pip install uv
```

### Local Development

Before deploying to Databricks, you can test the server locally:

1. **Install dependencies:**

```bash
uv sync
```

2. **Start the server locally:**

```bash
# Using UV
uv run mcp-sequentialthinking-databricks

# Or directly with uvicorn
uvicorn mcp_sequentialthinking_databricks.app:app --reload --host 0.0.0.0 --port 8000
```

3. **Access the server:**
   - Web interface: http://localhost:8000
   - MCP endpoint: http://localhost:8000/mcp/
   - Health check: http://localhost:8000/health

### Deploying to Databricks Apps

There are two methods to deploy the server on Databricks Apps:

#### Method 1: Using `databricks apps` CLI (Simpler)

This method is recommended for quick deployments and testing.

1. **Configure Databricks authentication:**

```bash
export DATABRICKS_CONFIG_PROFILE=<your-profile-name>  # e.g., my-databricks-profile
databricks auth login --profile "$DATABRICKS_CONFIG_PROFILE"
```

2. **Create a Databricks app:**

```bash
databricks apps create mcp-sequentialthinking-databricks
```

3. **Upload and deploy:**

```bash
# Get your Databricks username
DATABRICKS_USERNAME=$(databricks current-user me | jq -r .userName)

# Sync your code to Databricks workspace
databricks sync . "/Users/$DATABRICKS_USERNAME/mcp-sequentialthinking-databricks"

# Deploy the app
databricks apps deploy mcp-sequentialthinking-databricks \
  --source-code-path "/Workspace/Users/$DATABRICKS_USERNAME/mcp-sequentialthinking-databricks"
```

#### Method 2: Using `databricks bundle` CLI (Recommended for Production)

This method is better for production deployments and CI/CD pipelines.

1. **Configure Databricks authentication:**

```bash
export DATABRICKS_CONFIG_PROFILE=<your-profile-name>
databricks auth login --profile "$DATABRICKS_CONFIG_PROFILE"
```

2. **Build the wheel package:**

```bash
uv build --wheel
```

This creates a `.build` directory with:
- The Python wheel package
- `requirements.txt`
- `app.yaml`

3. **Deploy using Databricks bundles:**

```bash
# Deploy the bundle
databricks bundle deploy

# Run the app
databricks bundle run mcp-sequentialthinking-databricks
```

### Connecting to the Deployed MCP Server

Once deployed, you can connect to your MCP server using the **Streamable HTTP** transport.

1. **Get your app URL:**

After deployment, Databricks will provide a URL like:
```
https://your-app-url.cloud.databricks.com
```

2. **MCP Endpoint:**

Use the following URL for MCP connections:
```
https://your-app-url.cloud.databricks.com/mcp/
```

⚠️ **Important:** The URL must end with `/mcp/` (including the trailing slash) for the server to work correctly.

3. **Get authentication token:**

```bash
databricks auth token -p <name-of-your-profile>
```

4. **Configure your MCP client:**

Use the Streamable HTTP transport with:
- **URL:** `https://your-app-url.cloud.databricks.com/mcp/`
- **Authentication:** Bearer token from step 3

Example configuration for an MCP client:
```json
{
  "mcpServers": {
    "sequentialthinking-databricks": {
      "transport": "streamable-http",
      "url": "https://your-app-url.cloud.databricks.com/mcp/",
      "auth": {
        "type": "bearer",
        "token": "your-databricks-token"
      }
    }
  }
}
```

### Environment Variables

You can configure the server behavior using environment variables:

- `MAX_HISTORY_SIZE`: Maximum number of thoughts to retain (default: 1000)

To set environment variables in Databricks Apps, update the `app.yaml`:

```yaml
command: ["python", "-m", "mcp_sequentialthinking_databricks.main"]
env:
  - name: MAX_HISTORY_SIZE
    value: "2000"
```

### Monitoring and Debugging

1. **View logs:**

```bash
databricks apps logs mcp-sequentialthinking-databricks
```

2. **Check app status:**

```bash
databricks apps list
```

3. **Access health endpoint:**

```bash
curl https://your-app-url.cloud.databricks.com/health
```

### Updating the Deployment

To update an existing deployment:

```bash
# Rebuild the wheel
uv build --wheel

# Redeploy
databricks bundle deploy
databricks bundle run mcp-sequentialthinking-databricks
```

### Uninstalling

To remove the app from Databricks:

```bash
databricks apps delete mcp-sequentialthinking-databricks
```

## Development

### TypeScript Version (Original)

#### Setup

1. Clone the repository
2. Install dependencies:

```bash
pnpm install
```

3. Build the project:

```bash
pnpm build
```

4. Run in development mode:

```bash
pnpm dev
```

#### Publishing

The project uses changesets for version management. To publish:

1. Create a changeset:

```bash
pnpm changeset
```

2. Version the package:

```bash
pnpm changeset version
```

3. Publish to npm:

```bash
pnpm release
```

### Python Version (Databricks)

#### Setup

1. Clone the repository
2. Install dependencies:

```bash
uv sync
```

3. Run the server locally:

```bash
uv run mcp-sequentialthinking-databricks
```

Or with auto-reload for development:

```bash
uvicorn mcp_sequentialthinking_databricks.app:app --reload
```

#### Testing

Test the MCP tool locally:

```bash
# Test health endpoint
curl http://localhost:8000/health

# Access web interface
open http://localhost:8000
```

#### Building

Build the wheel package for Databricks:

```bash
uv build --wheel
```

This creates the distributable package in the `dist/` directory and a Databricks-compatible build in the `.build/` directory.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built on the
  [Model Context Protocol](https://github.com/modelcontextprotocol)
- Adapted from the
  [MCP Sequential Thinking Server](https://github.com/modelcontextprotocol/servers/blob/main/src/sequentialthinking/index.ts)
- Databricks deployment template from
  [custom_mcp_server_databricks](https://github.com/murtihash94/custom_mcp_server_databricks)

## Architecture

### Original (TypeScript/Node.js)
- Built with `tmcp` and `valibot`
- Uses stdio transport for local MCP communication
- Suitable for desktop MCP clients like Claude Desktop and Cline

### Databricks Version (Python/FastAPI)
- Built with `FastMCP` and `pydantic`
- Uses Streamable HTTP transport for web-based MCP communication
- Deployed as a Databricks App with uvicorn
- Includes web interface for status and monitoring
- Production-ready with health checks and logging

Both versions implement the same core sequential thinking logic and tool recommendation features.
