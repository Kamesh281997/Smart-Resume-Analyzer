
# ui/resume_upload.py
import streamlit as st
import uuid
import json

def render_upload_ui(extract_text_callback, summarize_callback, extract_entities_callback, 
                     embedding_callback, vector_store, db):
    """Render the resume upload UI"""
    st.header("Upload Resume")
    
    uploaded_file = st.file_uploader("Choose a resume file", type=["pdf", "docx"])
    
    if uploaded_file is not None:
        with st.spinner("Processing resume..."):
            # Extract text from resume
            resume_text = extract_text_callback(uploaded_file)
            
            # Generate resume ID
            resume_id = str(uuid.uuid4())
            
            # Store resume text in session state
            st.session_state.current_resume = uploaded_file.name
            st.session_state.resume_text = resume_text
            
            # Create tabs for different views
            tab1, tab2, tab3 = st.tabs(["Resume Text", "Summary", "Extracted Information"])
            
            with tab1:
                st.subheader("Extracted Text")
                st.text_area("Resume Content", resume_text, height=400, disabled=True)
            
            with tab2:
                st.subheader("Resume Summary")
                if st.button("Generate Summary"):
                    with st.spinner("Generating summary..."):
                        summary = summarize_callback(resume_text)
                        st.session_state.resume_summary = summary
                
                if "resume_summary" in st.session_state and st.session_state.resume_summary:
                    st.markdown(st.session_state.resume_summary)
            
            with tab3:
                st.subheader("Extracted Information")
                if st.button("Extract Structured Data"):
                    with st.spinner("Extracting information..."):
                        entities = extract_entities_callback(resume_text)
                        st.session_state.entities = entities
                        
                        # Display extracted information
                        if "BasicInformation" in entities:
                            st.write("Basic Information")
                            st.json(entities["BasicInformation"])
                        
                        if "Skills" in entities:
                            st.write("Skills")
                            st.json(entities["Skills"])
                        
                        if "Education" in entities:
                            st.write("Education")
                            st.json(entities["Education"])
                        
                        if "WorkExperience" in entities:
                            st.write("Work Experience")
                            st.json(entities["WorkExperience"])
                        
                        # Store in database
                        if db.connect():
                            basic_info = entities.get("BasicInformation", {})
                            skills = entities.get("Skills", [])
                            education = entities.get("Education", [])
                            experience = entities.get("WorkExperience", [])
                            
                            success = db.store_resume_data(
                                resume_id,
                                basic_info.get("FullName", ""),
                                basic_info.get("Email", ""),
                                basic_info.get("Phone", ""),
                                skills,
                                education,
                                experience,
                                st.session_state.get("resume_summary", "")
                            )
                            
                            if success:
                                st.success("Resume data stored in database successfully!")
                            else:
                                st.error("Failed to store resume data in database.")
                        else:
                            st.error("Failed to connect to database.")
            
            # Add resume to vector store
            if st.button("Add to Vector Store for Q&A"):
                with st.spinner("Adding to vector store..."):
                    # Get embeddings
                    embedding = embedding_callback(resume_text)
                    
                    # Add to vector store
                    doc_id = vector_store.add_document(
                        text=resume_text,
                        embedding=embedding,
                        metadata={
                            "resume_id": resume_id,
                            "filename": uploaded_file.name
                        }
                    )
                    
                    st.success(f"Resume added to vector store with ID: {doc_id}")
