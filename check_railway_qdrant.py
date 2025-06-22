#!/usr/bin/env python3

import asyncio
from qdrant_client import AsyncQdrantClient

async def check_railway_qdrant():
    # Your Railway environment variables
    qdrant_url = "https://01112caa-2452-44ce-a88e-221200aec8df.eu-central-1-0.aws.cloud.qdrant.io:6333"
    api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.bM5q2APkB8IETD-Hp_dtZwZoBkdJgxQqrHgIXZrIRbo"
    collection_name = "memory"
    
    client = AsyncQdrantClient(location=qdrant_url, api_key=api_key)
    
    try:
        # List all collections
        print("=== All Collections ===")
        collections = await client.get_collections()
        for collection in collections.collections:
            print(f"Collection: {collection.name}")
        
        # Check if the memory collection exists
        collection_exists = await client.collection_exists(collection_name)
        print(f"\nCollection '{collection_name}' exists: {collection_exists}")
        
        if collection_exists:
            # Get collection info
            print(f"\n=== Collection '{collection_name}' Details ===")
            collection_info = await client.get_collection(collection_name)
            print(f"Status: {collection_info.status}")
            print(f"Points count: {collection_info.points_count}")
            
            # Check vector configuration - this is the key part
            print(f"\n=== Vector Names in Collection ===")
            vectors_config = collection_info.config.params.vectors
            
            if isinstance(vectors_config, dict):
                for vector_name, vector_config in vectors_config.items():
                    print(f"Vector name: '{vector_name}'")
                    print(f"  Size: {vector_config.size}")
                    print(f"  Distance: {vector_config.distance}")
            else:
                print(f"Single vector config: {vectors_config}")
                
            # Try to get a few sample points to see the structure
            print(f"\n=== Sample Points ===")
            try:
                points = await client.scroll(
                    collection_name=collection_name,
                    limit=3,
                    with_payload=True,
                    with_vectors=True
                )
                
                for i, point in enumerate(points[0]):
                    print(f"Point {i+1}:")
                    print(f"  ID: {point.id}")
                    if hasattr(point, 'vector') and point.vector:
                        if isinstance(point.vector, dict):
                            for vec_name in point.vector.keys():
                                print(f"  Vector name in point: '{vec_name}'")
                        else:
                            print(f"  Vector type: {type(point.vector)}")
                    if hasattr(point, 'payload') and point.payload:
                        print(f"  Payload keys: {list(point.payload.keys())}")
                        
            except Exception as e:
                print(f"Could not retrieve sample points: {e}")
        
        else:
            print(f"Collection '{collection_name}' does not exist!")
            print("Available collections:")
            for collection in collections.collections:
                print(f"  - {collection.name}")
        
    except Exception as e:
        print(f"Error connecting to Qdrant: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(check_railway_qdrant())
