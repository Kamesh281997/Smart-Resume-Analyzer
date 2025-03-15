# schemas/database_schema.py

create_tables_queries = [
    """
    CREATE TABLE IF NOT EXISTS resumes (
        id TEXT PRIMARY KEY,
        name TEXT,
        email TEXT,
        phone TEXT,
        summary TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """,
    
    """
    CREATE TABLE IF NOT EXISTS skills (
        id SERIAL PRIMARY KEY,
        resume_id TEXT REFERENCES resumes(id) ON DELETE CASCADE,
        skill_name TEXT NOT NULL,
        UNIQUE(resume_id, skill_name)
    )
    """,
    
    """
    CREATE TABLE IF NOT EXISTS education (
        id SERIAL PRIMARY KEY,
        resume_id TEXT REFERENCES resumes(id) ON DELETE CASCADE,
        institution TEXT,
        degree TEXT,
        year_start INTEGER,
        year_end INTEGER
    )
    """,
    
    """
    CREATE TABLE IF NOT EXISTS experience (
        id SERIAL PRIMARY KEY,
        resume_id TEXT REFERENCES resumes(id) ON DELETE CASCADE,
        company TEXT,
        title TEXT,
        year_start INTEGER,
        year_end INTEGER,
        description TEXT
    )
    """
]
