import streamlit as st
from app import generate_idea, register_post, post_list_view, edit_post


# --- URLパラメータからページ名を取得（例：?page=投稿登録） ---
page = st.query_params.get("page", None)

# --- 投稿登録ページはサイドバーなしで表示 ---
if page == "投稿登録":
    register_post.render()

else:
    st.sidebar.title("📂 メニュー")
    selected_page = st.sidebar.radio("ページを選ぶ", ["投稿ネタ生成", "投稿登録", "投稿一覧"])

    if selected_page == "投稿ネタ生成":
        generate_idea.render()
    elif selected_page == "投稿登録":
        register_post.render()
    elif selected_page == "投稿一覧":
        post_list_view.render()

    # 編集ページ（セッションベース）
    if "edit_post_id" in st.session_state:
        edit_post.render()
