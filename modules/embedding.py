
# modules/embedding.py
import os
import groq
from typing import List
from sentence_transformers import SentenceTransformer



def get_embeddings(text: str) -> List[float]:
    """Generate embeddings using SentenceTransformer"""
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Check if text is too long and chunk if necessary
    max_chunk_length = 512  # SentenceTransformer models typically have token limits
    
    # Simple approach: if text seems long, chunk it
    if len(text.split()) > max_chunk_length:
        # Split text into sentences or paragraphs
        chunks = [s.strip() for s in text.split('.') if s.strip()]
        
        # Get embeddings for each chunk
        embeddings = model.encode(chunks)
        
        # Average the embeddings (simple approach)
        import numpy as np
        combined_embedding = np.mean(embeddings, axis=0)
        return combined_embedding.tolist()
    else:
        # For shorter texts, just get the embedding directly
        embedding = model.encode(text)
        return embedding.tolist()