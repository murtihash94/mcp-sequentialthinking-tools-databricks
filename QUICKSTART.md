# Quick Start Guide - Databricks Deployment

This guide provides a quick reference for deploying the MCP Sequential Thinking Tools to Databricks Apps.

## Prerequisites Checklist

- [ ] Databricks CLI installed
- [ ] UV installed (`pip install uv`)
- [ ] Python 3.11+
- [ ] Access to Databricks workspace
- [ ] Databricks authentication configured

## Installation Commands

```bash
# Install Databricks CLI (choose one)
curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sh
# OR
pip install databricks-cli

# Install UV
pip install uv
```

## Local Development (5 minutes)

```bash
# 1. Install dependencies
uv sync

# 2. Start server
uv run mcp-sequentialthinking-databricks

# 3. Test in browser
# Open: http://localhost:8000
```

## Quick Databricks Deployment (10 minutes)

### Method 1: Simple Deploy (Recommended for first-time users)

```bash
# Step 1: Authenticate
export DATABRICKS_CONFIG_PROFILE=my-profile
databricks auth login --profile "$DATABRICKS_CONFIG_PROFILE"

# Step 2: Create app
databricks apps create mcp-sequentialthinking-databricks

# Step 3: Deploy
DATABRICKS_USERNAME=$(databricks current-user me | jq -r .userName)
databricks sync . "/Users/$DATABRICKS_USERNAME/mcp-sequentialthinking-databricks"
databricks apps deploy mcp-sequentialthinking-databricks \
  --source-code-path "/Workspace/Users/$DATABRICKS_USERNAME/mcp-sequentialthinking-databricks"
```

### Method 2: Bundle Deploy (Recommended for production)

```bash
# Step 1: Authenticate
export DATABRICKS_CONFIG_PROFILE=my-profile
databricks auth login --profile "$DATABRICKS_CONFIG_PROFILE"

# Step 2: Build and deploy
uv build --wheel
databricks bundle deploy
databricks bundle run mcp-sequentialthinking-databricks
```

## Getting Your App URL

After deployment, Databricks provides an app URL:

```bash
# List your apps to get the URL
databricks apps list

# Look for: https://your-workspace.cloud.databricks.com/apps/your-app-id
```

## Connecting to Your Deployed Server

### MCP Endpoint

```
https://your-app-url.cloud.databricks.com/mcp/
```

⚠️ **Important:** Must include trailing slash `/mcp/`

### Get Authentication Token

```bash
databricks auth token -p <your-profile-name>
```

### Configure MCP Client

```json
{
  "mcpServers": {
    "sequentialthinking-databricks": {
      "transport": "streamable-http",
      "url": "https://your-app-url.cloud.databricks.com/mcp/",
      "auth": {
        "type": "bearer",
        "token": "your-databricks-token-here"
      }
    }
  }
}
```

## Verification Steps

```bash
# 1. Check deployment status
databricks apps list

# 2. View logs
databricks apps logs mcp-sequentialthinking-databricks

# 3. Test health endpoint
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://your-app-url.cloud.databricks.com/health

# Expected output:
# {
#   "status": "healthy",
#   "service": "mcp-sequential-thinking-tools",
#   "version": "0.0.4"
# }
```

## Common Commands

```bash
# View logs
databricks apps logs mcp-sequentialthinking-databricks

# Update deployment
uv build --wheel && databricks bundle deploy && databricks bundle run mcp-sequentialthinking-databricks

# Delete app
databricks apps delete mcp-sequentialthinking-databricks

# Check current user
databricks current-user me
```

## Troubleshooting

### Issue: Authentication failed
**Solution:** Re-run authentication
```bash
databricks auth login --profile "$DATABRICKS_CONFIG_PROFILE"
```

### Issue: App URL not accessible
**Solution:** Check app status and logs
```bash
databricks apps list
databricks apps logs mcp-sequentialthinking-databricks
```

### Issue: Build failed
**Solution:** Clean and rebuild
```bash
rm -rf dist/ .build/ *.egg-info
uv build --wheel
```

### Issue: Can't find `jq` command
**Solution:** Install jq or get username manually
```bash
# Install jq
sudo apt-get install jq  # Linux
brew install jq          # macOS

# Or manually
databricks current-user me
# Copy the userName field manually
```

## Environment Variables

Configure in `app.yaml`:

```yaml
command: ["python", "-m", "mcp_sequentialthinking_databricks.main"]
env:
  - name: MAX_HISTORY_SIZE
    value: "2000"
```

## Next Steps

1. ✅ Server deployed? → Test with MCP client
2. ✅ MCP client connected? → Run sequential thinking workflows
3. ✅ Need updates? → Follow "Update deployment" command above
4. ❓ Need help? → Check [TESTING.md](TESTING.md) and [README.md](README.md)

## Success Indicators

You're ready when you can:
- [ ] Access the web interface (https://your-app-url/)
- [ ] Get healthy response from /health endpoint
- [ ] Connect with MCP client using /mcp/ endpoint
- [ ] Execute the sequentialthinking_tools tool

---

**Time Investment:**
- Local setup: ~5 minutes
- First Databricks deploy: ~10 minutes
- Subsequent deploys: ~2 minutes

**Estimated Total:** 15-20 minutes from zero to fully deployed MCP server on Databricks! 🚀
