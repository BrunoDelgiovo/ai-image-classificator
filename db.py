import os
from dotenv import load_dotenv
import mysql.connector


def get_conn():
    # carrega .env (host, user, senha, db)
    load_dotenv()
    return mysql.connector.connect(
        host=os.getenv("db_host", "127.0.0.1"),
        port=int(os.getenv("db_port", "3306")),
        user=os.getenv("db_user", "root"),
        password=os.getenv("db_password", ""),
        database=os.getenv("db_name", "smartimg"),
    )


def insert_image(filename: str, sha256: str, description: str, category: str) -> int:
    # insere 1 linha na tabela e devolve  id
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        insert into images (filename, sha256, description, category)
        values (%s, %s, %s, %s)
        """,
        (filename, sha256, description, category),
    )

    conn.commit()
    new_id = cur.lastrowid

    cur.close()
    conn.close()
    return new_id


def find_by_sha256(sha256: str):
    # procura dupe pelo hash
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "select id, filename, category from images where sha256=%s limit 1",
        (sha256,),
    )
    row = cur.fetchone()

    cur.close()
    conn.close()
    return row


def list_images(limit: int = 10):
    # lista ultimos registros pra debug
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "select id, filename, category, created_at from images order by id desc limit %s",
        (limit,),
    )
    rows = cur.fetchall()

    cur.close()
    conn.close()
    return rows
