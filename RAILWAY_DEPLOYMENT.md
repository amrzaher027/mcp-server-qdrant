# Railway Deployment Guide for MCP Server Qdrant

This guide explains how to deploy the modified MCP Server Qdrant to Railway with proper host binding.

## Changes Made

The `src/mcp_server_qdrant/main.py` file has been modified to:
1. Accept `--host` and `--port` command line arguments
2. Automatically default to `0.0.0.0` (accessible from outside) instead of `127.0.0.1` (localhost only)
3. Ensure proper environment variable handling for Railway deployment

## Railway Configuration

### 1. Environment Variables
Set these in your Railway project's "Variables" tab:

```
QDRANT_URL=https://your-qdrant-cloud-url:6333
QDRANT_API_KEY=your_qdrant_api_key
COLLECTION_NAME=your_collection_name
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
FASTMCP_HOST=0.0.0.0
FASTMCP_PORT=8000
PORT=8000
```

### 2. Start Command Options

**Option A: Using explicit arguments (Recommended)**
```bash
uvx mcp-server-qdrant --transport sse --host 0.0.0.0 --port 8000
```

**Option B: Using environment variables only**
```bash
uvx mcp-server-qdrant --transport sse
```

### 3. Dockerfile (Alternative)
If you prefer using Docker, create a Dockerfile:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy the project files
COPY . .

# Install uv and the package
RUN pip install uv
RUN uv pip install --system -e .

# Set environment variables
ENV FASTMCP_HOST=0.0.0.0
ENV FASTMCP_PORT=8000

# Expose the port
EXPOSE 8000

# Start the server
CMD ["python", "-m", "mcp_server_qdrant.main", "--transport", "sse", "--host", "0.0.0.0", "--port", "8000"]
```

## Testing Your Deployment

### 1. Check Railway Logs
After deployment, check the logs. You should see:
```
INFO: Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```
Instead of:
```
INFO: Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

### 2. Test Connection
```bash
curl -I https://your-railway-app.railway.app/sse
```

Should return a successful HTTP response instead of 502 Bad Gateway.

### 3. AI Agent Connection
Configure your AI agent to use:
```
https://your-railway-app.railway.app/sse
```

## Local Testing

Run the test script to verify the changes work:
```bash
python test_server.py
```

This will start a local server on `0.0.0.0:8001` and verify it's accessible.

## Troubleshooting

### Still Getting 502 Bad Gateway?
1. Check Railway logs for startup errors
2. Verify all environment variables are set
3. Ensure the start command includes `--host 0.0.0.0`
4. Try the Dockerfile approach if uvx isn't working

### Server Not Starting?
1. Check for missing environment variables (especially QDRANT_URL or QDRANT_LOCAL_PATH)
2. Verify your Qdrant credentials are correct
3. Check Railway build logs for dependency installation issues

## Key Changes Summary

The main fix was ensuring the server binds to `0.0.0.0` (all interfaces) instead of `127.0.0.1` (localhost only). This allows Railway's load balancer to route external traffic to your application.

The modified `main.py` now:
- Accepts `--host` and `--port` arguments
- Defaults to `0.0.0.0` if no host is specified
- Properly sets FastMCP environment variables before importing the server
