import os
from dotenv import load_dotenv
import mysql.connector


def get_conn():
    load_dotenv()
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )


def insert_image(filename, sha256, description, category):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO images (filename, sha256, description, category)
        VALUES (%s, %s, %s, %s)
        """,
        (filename, sha256, description, category),
    )

    conn.commit()
    new_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return new_id


def list_images():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT id, filename, category FROM images")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows

def find_by_sha256(sha256):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, filename, category FROM images WHERE sha256=%s LIMIT 1",
        (sha256,)
    )

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return row
