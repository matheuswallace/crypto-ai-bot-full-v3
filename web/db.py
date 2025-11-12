import os
import psycopg
from psycopg.rows import dict_row

# Cria uma conexão global (pool) para reuso eficiente no Render
_connection = None


def get_connection():
    global _connection
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL não configurada")

    # Evita abrir várias conexões (Render fecha apps com excesso)
    if _connection is None or _connection.closed:
        _connection = psycopg.connect(db_url, sslmode="require", row_factory=dict_row)

    return _connection


def log_to_db(message: str):
    """
    Grava uma mensagem de log no banco PostgreSQL.
    Cria a tabela automaticamente se não existir.
    """
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id SERIAL PRIMARY KEY,
                    message TEXT,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """)
            cur.execute("INSERT INTO logs (message) VALUES (%s)", (message,))
            conn.commit()
    except Exception as e:
        print(f"[ERRO DB] Falha ao registrar log: {e}")
