import streamlit as st
import sqlite3
from datetime import datetime

# --- DB 接続 ---
conn = sqlite3.connect("db/posts.db", check_same_thread=False)
c = conn.cursor()

# --- 編集画面 ---
def render():
    st.subheader("✏ 投稿の編集")

    if "edit_post_id" not in st.session_state:
        st.info("編集する投稿が選ばれていません。")
        return

    post_id = st.session_state.edit_post_id
    c.execute("SELECT title, author_name, body, hashtags, post_date FROM posts WHERE id = ?", (post_id,))
    post = c.fetchone()

    if not post:
        st.error("指定された投稿が見つかりませんでした。")
        return

    title, author_name, body, hashtags, post_date = post

    with st.form("edit_form"):
        new_title = st.text_input("投稿タイトル", value=title)
        new_author = st.text_input("担当者名", value=author_name)
        new_body = st.text_area("投稿本文", value=body, height=200)
        new_hashtags = st.text_area("ハッシュタグ", value=hashtags)
        new_post_date = st.date_input("投稿日", value=datetime.strptime(post_date, "%Y-%m-%d"))

        submitted = st.form_submit_button("💾 編集内容を保存")

    if submitted:
        c.execute("""
            UPDATE posts
            SET title = ?, author_name = ?, body = ?, hashtags = ?, post_date = ?
            WHERE id = ?
        """, (new_title, new_author, new_body, new_hashtags, str(new_post_date), post_id))
        conn.commit()

        st.success("✅ 投稿内容を更新しました！")
        st.session_state.pop("edit_post_id", None)
        st.rerun()
