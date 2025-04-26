# utils/init_db.py
import sqlite3
import os

def initialize_database():
    os.makedirs("db", exist_ok=True)  # dbフォルダがなければ作る
    conn = sqlite3.connect("db/posts.db", check_same_thread=False)
    c = conn.cursor()

    # postsテーブルがなかったら作成
    c.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author_name TEXT,
            body TEXT,
            hashtags TEXT,
            post_date TEXT,
            created_at TEXT,
            status TEXT,
            thumbnail BLOB
        )
    """)

    # post_imagesテーブルがなかったら作成
    c.execute("""
        CREATE TABLE IF NOT EXISTS post_images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER,
            image BLOB,
            FOREIGN KEY(post_id) REFERENCES posts(id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()
