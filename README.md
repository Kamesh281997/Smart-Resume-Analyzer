# 📄 Resume RAG Application

An intelligent resume processing and exploration tool built using **Streamlit** and **LLMs**. This application allows users to upload resumes, automatically parse and summarize their contents, extract key information, store them in a **PostgreSQL** database, and even interact with them through a **RAG-based chat interface**.

---

## ✨ Key Features

- ✅ **Resume Upload & Parsing**: Upload resumes in PDF/DOCX formats and automatically extract their textual content.
- 🧠 **Smart Summarization**: Generate concise summaries using LLMs to understand a resume at a glance.
- 🏷️ **Entity Extraction**: Extract key metadata like names, skills, contact info, education, etc.
- 🔍 **Semantic Search & RAG Chatbot**: Query the resume content through a conversational chat interface powered by RAG (Retrieval-Augmented Generation).
- 🧾 **SQL Generation**: Dynamically generate SQL queries to explore the resume database using natural language.
- 💾 **Persistent Storage**: Store resumes and metadata securely in a PostgreSQL database.
- 📊 **Interactive Dashboard**: View uploaded resume data and query results in an intuitive UI.

---

## 🗂️ Project Structure

resume-rag-app/
├── app.py # Main Streamlit application
├── modules/ # Core business logic
│ ├── resume_parser.py # Resume parsing logic
│ ├── embedding.py # Text to embedding conversion
│ ├── vector_store.py # Vector store for RAG search
│ ├── database.py # PostgreSQL interface
│ ├── summarizer.py # Resume summarization
│ ├── entity_extractor.py # Extracts metadata from resume
│ ├── rag_engine.py # Chat engine for resume Q&A
│ └── sql_generator.py # Converts questions to SQL
├── ui/ # UI components (Streamlit pages)
│ ├── main_page.py
│ ├── resume_upload.py
│ ├── chat_interface.py
│ └── database_view.py
├── .env # Environment variables (not committed)
├── requirements.txt # Python dependencies
└── README.md

---

## ⚙️ Getting Started

### 1. Clone the Repository

git clone https://github.com/yourusername/resume-rag-app.git
cd resume-rag-app

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt

POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=resume_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yourpassword
GROQ_API_KEY=your_groq_api_key

📌 Future Enhancements
🔄 Integrate cloud vector databases (e.g., Pinecone, FAISS)

🔐 Add user authentication

🧩 Support multi-resume comparison

📁 Enable bulk upload and batch processing

📈 Add analytics for skill trends, education insights, etc.

☁️ Deploy to Streamlit Cloud or Docker environment
