
# ui/database_view.py
import streamlit as st
import pandas as pd

def render_database_ui(db, sql_generator):
    """Render the database view and query interface"""
    st.header("Database Interaction")
    
    # Connect to database if not already connected
    if not st.session_state.get("db_connected"):
        if db.connect():
            st.session_state.db_connected = True
            st.success("Connected to database successfully!")
        else:
            st.error("Failed to connect to database. Please check your credentials.")
            return
    
    # Create tabs for different query methods
    tab1, tab2 = st.tabs(["Natural Language Query", "SQL Query"])
    
    with tab1:
        st.subheader("Ask Questions About Resumes in Database")
        
        nl_query = st.text_input("Enter your question (e.g., 'Show me all candidates with Python skills')")
        
        if nl_query and st.button("Generate SQL and Run Query", key="nl_query_btn"):
            with st.spinner("Generating SQL query..."):
                # Generate SQL from natural language
                # ui/database_view.py (continued)
                # Generate SQL from natural language
                sql_result = sql_generator.generate_sql(nl_query)
                
                if sql_result["success"]:
                    st.code(sql_result["query"], language="sql")
                    
                    # Execute the generated query
                    with st.spinner("Executing query..."):
                        results = db.execute_query(sql_result["query"])
                        
                        if isinstance(results, list):
                            # Convert to DataFrame for better display
                            df = pd.DataFrame(results)
                            st.dataframe(df)
                        elif isinstance(results, dict) and "error" in results:
                            st.error(f"Error executing query: {results['error']}")
                        else:
                            st.success("Query executed successfully!")
                else:
                    st.error(sql_result["error"])
    
    with tab2:
        st.subheader("Custom SQL Query")
        
        # Show database schema information
        with st.expander("Database Schema"):
            st.code("""
            Tables:
            1. resumes (id TEXT, name TEXT, email TEXT, phone TEXT, summary TEXT, created_at TIMESTAMP)
            2. skills (id SERIAL, resume_id TEXT, skill_name TEXT)
            3. education (id SERIAL, resume_id TEXT, institution TEXT, degree TEXT, year_start INTEGER, year_end INTEGER)
            4. experience (id SERIAL, resume_id TEXT, company TEXT, title TEXT, year_start INTEGER, year_end INTEGER, description TEXT)
            """)
        
        # SQL query input
        sql_query = st.text_area("Enter SQL query", height=150)
        
        if sql_query and st.button("Run Query", key="sql_query_btn"):
            with st.spinner("Executing SQL query..."):
                results = db.execute_query(sql_query)
                
                if isinstance(results, list):
                    # Convert to DataFrame for better display
                    df = pd.DataFrame(results)
                    st.dataframe(df)
                elif isinstance(results, dict) and "error" in results:
                    st.error(f"Error executing query: {results['error']}")
                else:
                    st.success("Query executed successfully!")