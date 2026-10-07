from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql+psycopg2://postgres:8630911740@localhost:5432/cybersecurity_db"

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("PostgreSQL connection successful.")
        print("Test result:", result.scalar())

except Exception as e:
    print("PostgreSQL connection failed.")
    print("Error:", e)