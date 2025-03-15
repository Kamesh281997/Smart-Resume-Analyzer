
# modules/database.py
import psycopg2
from psycopg2.extras import RealDictCursor
from schemas.database_schema import create_tables_queries

class PostgresDB:
    def __init__(self, host, port, database, user, password):
        self.connection_params = {
            "host": host,
            "port": port,
            "database": database,
            "user": user,
            "password": password
        }
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Connect to PostgreSQL database"""
        try:
            self.connection = psycopg2.connect(**self.connection_params)
            self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            self._init_db()
            return True
        except Exception as e:
            print(f"Error connecting to database: {e}")
            return False
    
    def _init_db(self):
        """Initialize database schema if not exists"""
        if self.connection and self.cursor:
            for query in create_tables_queries:
                self.cursor.execute(query)
            self.connection.commit()
    
    def store_resume_data(self, resume_id, name, email, phone, skills, education, experience, summary):
        """Store resume data in database"""
        if not self.connection:
            self.connect()
            
        try:
            # Insert basic info
            self.cursor.execute(
                """
                INSERT INTO resumes (id, name, email, phone, summary)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE
                SET name = EXCLUDED.name,
                    email = EXCLUDED.email,
                    phone = EXCLUDED.phone,
                    summary = EXCLUDED.summary
                RETURNING id
                """,
                (resume_id, name, email, phone, summary)
            )
            
            # Insert skills
            if skills:
                for skill in skills:
                    self.cursor.execute(
                        """
                        INSERT INTO skills (resume_id, skill_name)
                        VALUES (%s, %s)
                        ON CONFLICT (resume_id, skill_name) DO NOTHING
                        """,
                        (resume_id, skill)
                    )
            
            # Insert education
            if education:
                for edu in education:
                    self.cursor.execute(
                        """
                        INSERT INTO education (resume_id, institution, degree, year_start, year_end)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (resume_id, edu.get("institution"), edu.get("degree"), 
                         edu.get("year_start"), edu.get("year_end"))
                    )
            
            # Insert experience
            if experience:
                for exp in experience:
                    self.cursor.execute(
                        """
                        INSERT INTO experience (resume_id, company, title, year_start, year_end, description)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                        (resume_id, exp.get("company"), exp.get("title"), 
                         exp.get("year_start"), exp.get("year_end"), exp.get("description"))
                    )
            
            self.connection.commit()
            return True
            
        except Exception as e:
            self.connection.rollback()
            print(f"Error storing resume data: {e}")
            return False
    
    def execute_query(self, query):
        """Execute SQL query and return results"""
        if not self.connection:
            self.connect()
            
        try:
            self.cursor.execute(query)
            if query.strip().upper().startswith("SELECT"):
                return self.cursor.fetchall()
            else:
                self.connection.commit()
                return {"message": "Query executed successfully"}
        except Exception as e:
            self.connection.rollback()
            return {"error": str(e)}
    
    def close(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()