FROM python:3.11-slim

WORKDIR /app

# Copy the project files
COPY . .

# Install uv
RUN pip install uv

# Install the package from local source
RUN uv pip install --system -e .

# Set environment variables for Railway deployment
ENV FASTMCP_HOST=0.0.0.0
ENV FASTMCP_PORT=8000

# Expose the port
EXPOSE 8000

# Start the server with our modified code
CMD ["python", "-m", "mcp_server_qdrant.main", "--transport", "sse", "--host", "0.0.0.0", "--port", "8000"]
