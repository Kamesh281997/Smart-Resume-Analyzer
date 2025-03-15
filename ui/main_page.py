# ui/main_page.py
import streamlit as st

def render_main_page():
    """Render the main page layout"""
    st.title("Resume Analysis and Q&A System")
    st.markdown("""
    This application allows you to:
    - Upload resumes in PDF or DOCX format
    - Extract structured information from resumes
    - Ask questions about the resume content
    - Store resume data in a PostgreSQL database
    - Query the database using natural language
    """)
