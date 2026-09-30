from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg2://postgres:8630911740@localhost:5432/cybersecurity_db"

engine = create_engine(DATABASE_URL)

print("Database connection configuration loaded.")