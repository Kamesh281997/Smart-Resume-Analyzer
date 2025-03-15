
# modules/entity_extractor.py
import os
import groq
import json
from typing import Dict, List, Any

def extract_entities(text: str) -> Dict[str, Any]:
    """Extract structured information from resume using Groq API"""
    client = groq.Client(api_key=os.getenv("GROQ_API_KEY"))
    
    prompt = f"""
    Extract the following information from this resume in JSON format:
    
    1. Basic Information:
       - Full Name
       - Email
       - Phone
    
    2. Skills: List of all technical and soft skills mentioned
    
    3. Education: List of education entries, each containing:
       - Institution
       - Degree/Certification
       - Year Started (if available)
       - Year Completed/Expected (if available)
    
    4. Work Experience: List of work experiences, each containing:
       - Company Name
       - Job Title
       - Start Year
       - End Year (or "Present")
       - Brief Description
    
    Resume:
    {text}
    
    Respond ONLY with a valid JSON object. Do not include any explanations or text outside the JSON.
    """
    
    response = client.chat.completions.create(
        model="llama3-70b-8192",  # Use appropriate model
        messages=[
            {"role": "system", "content": "You are a resume parsing expert. Extract structured information from resumes."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        max_tokens=2000
    )
    
    try:
        # Parse JSON response
        result = json.loads(response.choices[0].message.content)
        return result
    except json.JSONDecodeError:
        # If JSON parsing fails, attempt to extract the JSON part
        content = response.choices[0].message.content
        
        # Try to find JSON between triple backticks
        if "```json" in content and "```" in content.split("```json", 1)[1]:
            json_part = content.split("```json", 1)[1].split("```", 1)[0]
            try:
                return json.loads(json_part)
            except json.JSONDecodeError:
                pass
                
        # Return a basic structure if JSON parsing fails
        return {
            "BasicInformation": {
                "FullName": "",
                "Email": "",
                "Phone": ""
            },
            "Skills": [],
            "Education": [],
            "WorkExperience": []
        }
