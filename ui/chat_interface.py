
# ui/chat_interface.py
import streamlit as st

def render_chat_ui(rag_engine):
    """Render the chat interface for asking questions about resumes"""
    st.header("Chat with Resume")
    
    # Check if there's a resume in the vector store
    if not rag_engine.vector_store.documents:
        st.warning("No resumes have been added to the system. Please upload a resume first.")
        return
    
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # User input
    user_input = st.chat_input("Ask a question about the resume...")
    
    if user_input:
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Display user message
        with st.chat_message("user"):
            st.write(user_input)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = rag_engine.query(user_input, st.session_state.chat_history)
                st.write(response)
        
        # Add assistant response to chat history
        st.session_state.chat_history.append({"role": "assistant", "content": response})
