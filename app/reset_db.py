import streamlit as st
import sqlite3
import os

def render():
    st.subheader("🛠 データベース初期化")

    if st.button("⚠️ posts.db にテーブルを作成する"):
        try:
            os.makedirs("db", exist_ok=True)
            conn = sqlite3.connect("db/posts.db")
            c = conn.cursor()

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

            c.execute("""
            CREATE TABLE IF NOT EXISTS post_images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id INTEGER,
                image BLOB,
                FOREIGN KEY(post_id) REFERENCES posts(id)
            )
            """)

            conn.commit()
            conn.close()

            st.success("✅ 初期化が完了しました！")
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
