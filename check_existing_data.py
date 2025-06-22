#!/usr/bin/env python3

import asyncio
from qdrant_client import AsyncQdrantClient

async def check_existing_data():
    # Your Railway environment variables
    qdrant_url = "https://01112caa-2452-44ce-a88e-221200aec8df.eu-central-1-0.aws.cloud.qdrant.io:6333"
    api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.bM5q2APkB8IETD-Hp_dtZwZoBkdJgxQqrHgIXZrIRbo"
    collection_name = "memory"
    
    client = AsyncQdrantClient(location=qdrant_url, api_key=api_key)
    
    try:
        # Get the existing point to see its structure
        points = await client.scroll(
            collection_name=collection_name,
            limit=1,
            with_payload=True,
            with_vectors=False  # Don't need the actual vector data
        )
        
        if points[0]:
            point = points[0][0]
            print("=== Existing Point Structure ===")
            print(f"Point ID: {point.id}")
            print(f"Payload keys: {list(point.payload.keys())}")
            print("\n=== Payload Content ===")
            for key, value in point.payload.items():
                if isinstance(value, str) and len(value) > 100:
                    print(f"{key}: {value[:100]}...")
                else:
                    print(f"{key}: {value}")
                    
            # Check if there's a 'document' field that the current code expects
            if 'document' in point.payload:
                print(f"\n✓ Found 'document' field - compatible with current code")
            else:
                print(f"\n⚠ No 'document' field found - need to adapt search logic")
                
            # Check for full_text field which might be the main content
            if 'full_text' in point.payload:
                print(f"✓ Found 'full_text' field - this might be the main content")
                
        else:
            print("No points found in collection")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(check_existing_data())
