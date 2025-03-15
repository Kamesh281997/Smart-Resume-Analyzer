import os
import groq
from typing import List, Dict, Any

def generate_summary(text: str) -> str:
    """Generate a summary of the resume using Groq API"""
    client = groq.Client(api_key=os.getenv("GROQ_API_KEY"))
    
    prompt = f"""
    You are a professional resume analyzer. Your task is to create a concise summary of the following resume.
    The summary should highlight the candidate's key qualifications, skills, experience, and education.
    Keep the summary under 300 words and focus on the most relevant aspects.
    
    Resume:
    {text}
    
    Summary:
    """
    
    response = client.chat.completions.create(
        model="llama3-70b-8192",  # Use appropriate model
        messages=[
            {"role": "system", "content": "You are a professional resume analyzer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=500
    )
    
    return response.choices[0].message.content