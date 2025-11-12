import os
import psycopg2

def get_connection():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL não configurada")
    return psycopg2.connect(db_url, sslmode="require")

def log_to_db(message):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS logs (id SERIAL PRIMARY KEY, message TEXT, created_at TIMESTAMP DEFAULT NOW())")
    cur.execute("INSERT INTO logs (message) VALUES (%s)", (message,))
    conn.commit()
    cur.close()
    conn.close()
