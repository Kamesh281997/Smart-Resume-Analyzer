
# modules/sql_generator.py
import os
import groq
from typing import Dict

class SQLGenerator:
    def __init__(self, groq_api_key):
        self.groq_api_key = groq_api_key
        self.client = groq.Client(api_key=groq_api_key)
        
        # Database schema information for context
        self.schema_info = """
        Database Schema:
        
        1. resumes (id TEXT, name TEXT, email TEXT, phone TEXT, summary TEXT, created_at TIMESTAMP)
        2. skills (id SERIAL, resume_id TEXT, skill_name TEXT)
        3. education (id SERIAL, resume_id TEXT, institution TEXT, degree TEXT, year_start INTEGER, year_end INTEGER)
        4. experience (id SERIAL, resume_id TEXT, company TEXT, title TEXT, year_start INTEGER, year_end INTEGER, description TEXT)
        
        Relationships:
        - skills.resume_id references resumes.id
        - education.resume_id references resumes.id
        - experience.resume_id references resumes.id
        """
    
    def generate_sql(self, natural_language_query: str) -> Dict:
        """Generate SQL query from natural language question"""
        prompt = f"""
        Convert the following natural language question about resume data into a valid PostgreSQL query.
        
        {self.schema_info}
        
        Question: {natural_language_query}
        
        Write ONLY the SQL query without any explanation or commentary. The query should be well-formatted, 
        secure, and efficient. If the question cannot be translated into SQL with the given schema, 
        respond with "Cannot translate to SQL: [brief reason]".
        """
        
        response = self.client.chat.completions.create(
            model="llama3-70b-8192",  # Use appropriate model
            messages=[
                {"role": "system", "content": "You are an expert SQL generator that translates natural language questions into PostgreSQL queries."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=500
        )
        
        sql_query = response.choices[0].message.content.strip()
        
        # Check if it's an error message or a valid SQL query
        if sql_query.startswith("Cannot translate to SQL:"):
            return {
                "success": False,
                "error": sql_query,
                "query": None
            }
        
        # Remove SQL code blocks if present
        if sql_query.startswith("```sql"):
            sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
        elif sql_query.startswith("```"):
            sql_query = sql_query.replace("```", "").strip()
        
        return {
            "success": True,
            "query": sql_query,
            "error": None
        }