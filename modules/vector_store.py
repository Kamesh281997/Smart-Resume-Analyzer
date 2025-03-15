
# modules/vector_store.py
import faiss
import numpy as np
import pickle
import os
from typing import List, Dict, Any

class VectorStore:
    def __init__(self, dimension: int = 384):  # Adjust dimension based on embedding model
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.documents = []  # Store document texts
        self.metadata = []   # Store document metadata
    
    def add_document(self, text: str, embedding: List[float], metadata: Dict[str, Any] = None):
        """Add document to vector store"""
        if metadata is None:
            metadata = {}
        
        # Convert embedding to numpy array
        embedding_np = np.array(embedding, dtype=np.float32).reshape(1, self.dimension)
    
        # Add to FAISS index
        self.index.add(embedding_np)
        
        # Store the document and metadata
        self.documents.append(text)
        self.metadata.append(metadata)
        
        
        # Store document and metadata
        doc_id = len(self.documents)
        # self.documents.append(text)
        # self.metadata.append({"id": doc_id, **metadata})
        
        return doc_id
    
    def search(self, query_embedding: List[float], k: int = 5):
        """Search for similar documents"""
        # Convert query embedding to numpy array
        query_np = np.array([query_embedding], dtype=np.float32)
        
        # Search in FAISS index
        distances, indices = self.index.search(query_np, k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1 and idx < len(self.documents):
                results.append({
                    "document": self.documents[idx],
                    "metadata": self.metadata[idx],
                    "distance": float(distances[0][i])
                })
        
        return results
    
    def save(self, file_path: str):
        """Save vector store to disk"""
        # Save FAISS index
        faiss.write_index(self.index, f"{file_path}.index")
        
        # Save documents and metadata
        with open(f"{file_path}.pkl", "wb") as f:
            pickle.dump((self.documents, self.metadata), f)
    
    def load(self, file_path: str):
        """Load vector store from disk"""
        # Load FAISS index
        self.index = faiss.read_index(f"{file_path}.index")
        
        # Load documents and metadata
        with open(f"{file_path}.pkl", "rb") as f:
            self.documents, self.metadata = pickle.load(f)
