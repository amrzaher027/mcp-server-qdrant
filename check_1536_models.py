#!/usr/bin/env python3

from fastembed import TextEmbedding

# List available models and their dimensions
print("=== Available FastEmbed Models ===")
models = TextEmbedding.list_supported_models()

for model in models:
    if hasattr(model, 'dim') and model.dim == 1536:
        print(f"✓ {model.model}: {model.dim} dimensions")
    elif hasattr(model, 'dim'):
        print(f"  {model.model}: {model.dim} dimensions")
    else:
        print(f"  {model.model}: dimensions unknown")

print("\n=== Looking for 1536-dimensional models ===")
for model in models:
    if hasattr(model, 'dim') and model.dim == 1536:
        print(f"Found: {model.model} - {model.dim} dimensions")
