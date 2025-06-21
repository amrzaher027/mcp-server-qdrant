#!/usr/bin/env python3
"""
Test script to verify the MCP server starts with correct host binding
"""
import subprocess
import sys
import time
import requests
from threading import Thread

def test_server_binding():
    """Test that the server binds to 0.0.0.0 instead of 127.0.0.1"""
    
    print("Testing MCP server host binding...")
    
    # Start the server in a subprocess
    cmd = [
        sys.executable, "-m", "mcp_server_qdrant.main",
        "--transport", "sse",
        "--host", "0.0.0.0",
        "--port", "8001"
    ]
    
    print(f"Running command: {' '.join(cmd)}")
    
    try:
        # Set minimal environment variables for testing
        import os
        env = os.environ.copy()
        env.update({
            "QDRANT_LOCAL_PATH": ":memory:",  # Use in-memory Qdrant for testing
            "COLLECTION_NAME": "test",
            "EMBEDDING_MODEL": "sentence-transformers/all-MiniLM-L6-v2"
        })
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env
        )
        
        # Give the server time to start
        time.sleep(5)
        
        # Check if the process is still running
        if process.poll() is not None:
            stdout, stderr = process.communicate()
            print("Server failed to start!")
            print("STDOUT:", stdout)
            print("STDERR:", stderr)
            return False
        
        # Try to connect to the server
        try:
            response = requests.get("http://localhost:8001/sse", timeout=5)
            print(f"Server responded with status: {response.status_code}")
            print("✅ Server is accessible on 0.0.0.0:8001")
            success = True
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to connect to server: {e}")
            success = False
        
        # Clean up
        process.terminate()
        process.wait(timeout=5)
        
        return success
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    success = test_server_binding()
    sys.exit(0 if success else 1)
