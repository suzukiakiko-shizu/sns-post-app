import streamlit as st
import sqlite3
import io
from PIL import Image

# --- DB 接続 ---
conn = sqlite3.connect("db/posts.db", check_same_thread=False)
c = conn.cursor()

# --- 投稿一覧画面 ---
def render():
    st.subheader("📋 投稿一覧")

    # ステータスフィルター
    status_filter = st.selectbox("表示するステータスを選択", ["すべて", "未承認", "承認済み", "予約済み", "投稿完了"], index=0)

    # 社長モード切替
    st.sidebar.markdown("---")
    st.sidebar.checkbox("👑 社長モード", key="is_president")

    c.execute("SELECT id, title, author_name, body, hashtags, post_date, created_at, status, thumbnail FROM posts ORDER BY created_at DESC")
    posts = c.fetchall()

    if status_filter != "すべて":
        posts = [post for post in posts if post[7] == status_filter]

    if not posts:
        st.info("まだ投稿がありません。")
        return

    for post in posts:
        post_id, title, author_name, body, hashtags, post_date, created_at, status, thumbnail = post

        if status == "未承認":
            status_color = "gray"
        elif status == "承認済み":
            status_color = "blue"
        elif status == "予約済み":
            status_color = "orange"
        elif status == "投稿完了":
            status_color = "green"
        else:
            status_color = "lightgray"
        status_badge = f"<span style='background-color:{status_color}; color:white; padding:2px 8px; border-radius:10px;'>{status}</span>"

        # タイトル見出しを強調表示
        st.markdown(f"### 📝 {title or '（タイトルなし）'} {status_badge}", unsafe_allow_html=True)

        with st.expander(f"{created_at.split(' ')[0]}（作成日）", expanded=False):
            st.markdown(f"**投稿予定日**：{post_date}")
            st.markdown(f"**担当者**：{author_name or '未入力'}")
            st.markdown(f"**本文**：\n{body}")
            st.markdown(f"**ハッシュタグ**：{hashtags}")

            if thumbnail:
                image = Image.open(io.BytesIO(thumbnail))
                st.image(image, caption="サムネイル画像", use_container_width=True)

            # 投稿画像一覧
            c.execute("SELECT image FROM post_images WHERE post_id = ?", (post_id,))
            images = c.fetchall()
            if images:
                st.markdown("**投稿画像：**")
                for i, (img_bytes,) in enumerate(images):
                    image = Image.open(io.BytesIO(img_bytes))
                    st.image(image, caption=f"画像 {i+1}", use_container_width=True)

            # ステータス変更（スタッフが予約済み・投稿完了に変更）
            if status in ["承認済み", "予約済み"]:
                new_status = st.selectbox(
                    "📌 ステータス変更",
                    ["承認済み", "予約済み", "投稿完了"],
                    index=["承認済み", "予約済み", "投稿完了"].index(status),
                    key=f"status_select_{post_id}"
                )
                if new_status != status:
                    if st.button("💾 ステータスを更新", key=f"update_status_{post_id}"):
                        c.execute("UPDATE posts SET status = ? WHERE id = ?", (new_status, post_id))
                        conn.commit()
                        st.success(f"✅ ステータスを『{new_status}』に更新しました！")
                        st.rerun()

            # 操作ボタン：編集、承認、削除
            st.markdown("---")
            col_op1, col_op2, col_op3 = st.columns(3)
            with col_op1:
                if st.button("✏ 編集", key=f"edit_{post_id}"):
                    st.session_state.edit_post_id = post_id
                    st.rerun()
            with col_op2:
                if st.session_state.get("is_president") and status == "未承認":
                    if st.button("✅ 承認する", key=f"approve_{post_id}"):
                        c.execute("UPDATE posts SET status = '承認済み' WHERE id = ?", (post_id,))
                        conn.commit()
                        st.success("✅ 投稿を承認しました！")
                        st.rerun()
            with col_op3:
                if st.button("🗑 削除", key=f"delete_{post_id}"):
                    st.session_state.confirm_delete_id = post_id

            # 削除確認
            if st.session_state.get("confirm_delete_id") == post_id:
                st.warning("⚠️ この投稿を本当に削除しますか？")
                col_confirm1, col_confirm2 = st.columns(2)
                with col_confirm1:
                    if st.button("✅ はい、削除する", key=f"confirm_yes_{post_id}"):
                        c.execute("DELETE FROM post_images WHERE post_id = ?", (post_id,))
                        c.execute("DELETE FROM posts WHERE id = ?", (post_id,))
                        conn.commit()
                        st.success("✅ 投稿を削除しました！")
                        st.session_state.pop("confirm_delete_id")
                        st.rerun()
                with col_confirm2:
                    if st.button("キャンセル", key=f"confirm_no_{post_id}"):
                        st.session_state.pop("confirm_delete_id")
                        st.info("削除をキャンセルしました。")
