#!/usr/bin/env python3

import asyncio
import os
from qdrant_client import AsyncQdrantClient

async def debug_qdrant():
    # Your Railway environment variables
    qdrant_url = "https://01112caa-2452-44ce-a88e-221200aec8df.eu-central-1-0.aws.cloud.qdrant.io:6333"
    api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.bM5q2APkB8IETD-Hp_dtZwZoBkdJgxQqrHgIXZrIRbo"
    collection_name = "memory"
    
    client = AsyncQdrantClient(location=qdrant_url, api_key=api_key)
    
    try:
        # List all collections
        print("=== Collections ===")
        collections = await client.get_collections()
        for collection in collections.collections:
            print(f"Collection: {collection.name}")
        
        # Check if the specific collection exists
        collection_exists = await client.collection_exists(collection_name)
        print(f"\nCollection '{collection_name}' exists: {collection_exists}")
        
        if collection_exists:
            # Get collection info
            print(f"\n=== Collection '{collection_name}' Info ===")
            collection_info = await client.get_collection(collection_name)
            print(f"Status: {collection_info.status}")
            print(f"Vectors count: {collection_info.vectors_count}")
            print(f"Points count: {collection_info.points_count}")
            
            # Check vector configuration
            print(f"\n=== Vector Configuration ===")
            if hasattr(collection_info.config, 'params') and hasattr(collection_info.config.params, 'vectors'):
                vectors_config = collection_info.config.params.vectors
                if isinstance(vectors_config, dict):
                    for vector_name, vector_config in vectors_config.items():
                        print(f"Vector name: '{vector_name}'")
                        print(f"  Size: {vector_config.size}")
                        print(f"  Distance: {vector_config.distance}")
                else:
                    print(f"Vectors config type: {type(vectors_config)}")
                    print(f"Vectors config: {vectors_config}")
            else:
                print("Could not access vector configuration")
                print(f"Collection config: {collection_info.config}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(debug_qdrant())
