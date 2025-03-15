import streamlit as st
import os
from dotenv import load_dotenv

# Import necessary modules
from modules.resume_parser import extract_text_from_resume
from modules.embedding import get_embeddings
from modules.vector_store import VectorStore
from modules.database import PostgresDB
from modules.summarizer import generate_summary
from modules.entity_extractor import extract_entities
from modules.rag_engine import RAGEngine
from modules.sql_generator import SQLGenerator

# Import UI components
from ui.main_page import render_main_page
from ui.resume_upload import render_upload_ui
from ui.chat_interface import render_chat_ui
from ui.database_view import render_database_ui

# Load environment variables
load_dotenv()

# App title and configuration
st.set_page_config(
    page_title="Resume RAG Application",
    page_icon="📄",
    layout="wide"
)

# Initialize session state
if "current_resume" not in st.session_state:
    st.session_state.current_resume = None
if "resume_text" not in st.session_state:
    st.session_state.resume_text = None
if "resume_summary" not in st.session_state:
    st.session_state.resume_summary = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "db_connected" not in st.session_state:
    st.session_state.db_connected = False

# Initialize components
@st.cache_resource
def initialize_components():
    # Connect to PostgreSQL database
    db = PostgresDB(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        database=os.getenv("POSTGRES_DB", "resume_db"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres")
    )
    
    # Initialize vector store
    vector_store = VectorStore()
    
    # Initialize RAG engine
    rag_engine = RAGEngine(vector_store, os.getenv("GROQ_API_KEY"))
    print("os.getenv(GROQ_API_KEY): ",os.getenv("GROQ_API_KEY"))
    # Initialize SQL generator
    sql_generator = SQLGenerator(os.getenv("GROQ_API_KEY"))
    
    return db, vector_store, rag_engine, sql_generator

# Main application
def main():
    db, vector_store, rag_engine, sql_generator = initialize_components()
    
    # Render main layout with sidebar navigation
    render_main_page()
    
    # Navigation
    page = st.sidebar.radio("Navigation", ["Upload Resume", "Chat with Resume", "Database View"])
    
    if page == "Upload Resume":
        render_upload_ui(
            extract_text_callback=extract_text_from_resume,
            summarize_callback=generate_summary,
            extract_entities_callback=extract_entities,
            embedding_callback=get_embeddings,
            vector_store=vector_store,
            db=db
        )
    
    elif page == "Chat with Resume":
        render_chat_ui(rag_engine)
    
    elif page == "Database View":
        render_database_ui(db, sql_generator)

if __name__ == "__main__":
    main()