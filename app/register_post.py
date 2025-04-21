import streamlit as st
import sqlite3
import os
from datetime import datetime

# --- DB 接続（フォルダがなければ作成） ---
os.makedirs("data", exist_ok=True)
conn = sqlite3.connect("db/posts.db", check_same_thread=False)
c = conn.cursor()

# --- 投稿登録画面 ---
def render():
    st.subheader("📝 新規投稿の登録")

    # --- 編集フォーム ---
    with st.form("post_form"):
        title = st.text_input("1. 投稿タイトル")
        author_name = st.text_input("2. 担当者名")
        body = st.text_area("3. 投稿本文", height=200)

        thumbnail = st.file_uploader("4. サムネイル画像（1枚）", type=["png", "jpg", "jpeg"], accept_multiple_files=False)
        images = st.file_uploader("5. 投稿用画像（複数可）", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

        hashtags = st.text_area("6. ハッシュタグ（カンマ区切り or 改行）")
        post_date = st.date_input("7. 投稿日")

        submit = st.form_submit_button("💾 この内容で保存する")

    if submit:
        if not body:
            st.error("投稿本文は必須です。")
            return

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        thumbnail_data = thumbnail.read() if thumbnail else None

        try:
            c.execute("""
                INSERT INTO posts (title, author_name, body, hashtags, post_date, created_at, status, thumbnail)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                title,
                author_name,
                body,
                hashtags,
                str(post_date),
                created_at,
                "未承認",
                thumbnail_data
            ))
            post_id = c.lastrowid

            if images:
                for img in images:
                    img_data = img.read()
                    c.execute("""
                        INSERT INTO post_images (post_id, image)
                        VALUES (?, ?)
                    """, (post_id, img_data))

            conn.commit()
            st.success("✅ 投稿が保存されました！")
        except Exception as e:
            st.error(f"保存中にエラーが発生しました：{e}")
