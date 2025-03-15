
# modules/rag_engine.py
import os
import groq
import uuid
from typing import List, Dict, Any

class RAGEngine:
    def __init__(self, vector_store, groq_api_key):
        self.vector_store = vector_store
        self.groq_api_key = groq_api_key
        self.client = groq.Client(api_key=groq_api_key)
    
    def query(self, question: str, chat_history: List[Dict[str, str]] = None) -> str:
        """Process a query using RAG approach"""
        if chat_history is None:
            chat_history = []
        
        # Get embeddings for the question
        from modules.embedding import get_embeddings
        question_embedding = get_embeddings(question)
        
        # Search for relevant documents
        search_results = self.vector_store.search(question_embedding, k=3)
        
        # Prepare context from search results
        context = "\n\n".join([result["document"] for result in search_results])
        
        # Prepare messages for the LLM
        messages = [
            {
                "role": "system", 
                "content": """You are a helpful resume assistant that answers questions based on the provided resume content.
                Only answer questions based on the information in the resume. If the information is not available in the resume,
                say so clearly. Do not make up information that is not in the resume."""
            }
        ]
        
        # Add chat history for context
        for message in chat_history[-5:]:  # Only include last 5 messages to keep context manageable
            messages.append({"role": message["role"], "content": message["content"]})
        
        # Add current question with context
        messages.append({
            "role": "user", 
            "content": f"""
            Resume Information:
            {context}
            
            Question: {question}
            
            Please answer the question based only on the information available in the resume.
            """
        })
        
        # Get response from LLM
        response = self.client.chat.completions.create(
            model="llama3-70b-8192",  # Use appropriate model
            messages=messages,
            temperature=0.2,
            max_tokens=800
        )
        
        return response.choices[0].message.content
