#!/usr/bin/env python3

from fastembed import TextEmbedding

# Check the dimensions of the FastEmbed model
model_name = "sentence-transformers/all-MiniLM-L6-v2"
embedding_model = TextEmbedding(model_name)

# Get a sample embedding to check dimensions
sample_text = "test"
embeddings = list(embedding_model.query_embed([sample_text]))
print(f"Model: {model_name}")
print(f"Embedding dimensions: {len(embeddings[0])}")

# Also check the model description
from fastembed.common.model_description import DenseModelDescription
model_description = embedding_model._get_model_description(model_name)
print(f"Model description dimensions: {model_description.dim}")
