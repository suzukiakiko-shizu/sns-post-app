import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
from utils.categories import TARGET_CATEGORIES, PURPOSE_CATEGORIES, FORMAT_CATEGORIES
from utils.ai_prompts import build_post_content_prompt
import urllib.parse

# --- API キーの読み込み ---
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def render():
    st.subheader("🧠 投稿ネタと条件を指定して投稿案を一括生成")

    # --- 入力フォーム ---
    with st.form("input_form"):
        topic = st.text_input("投稿ネタ（例：メロンクリームソーダ、決起大会レポート）", "")
        col1, col2, col3 = st.columns(3)
        target = col1.selectbox("想定ターゲット", TARGET_CATEGORIES)
        purpose = col2.selectbox("投稿の目的", PURPOSE_CATEGORIES)
        format_type = col3.selectbox("投稿形式", FORMAT_CATEGORIES)
        submitted = st.form_submit_button("投稿案を生成する")

    # --- 投稿案生成処理 ---
    if submitted and topic:
        with st.spinner("投稿案を生成中..."):
            prompt = build_post_content_prompt(topic, target, purpose, format_type)
            try:
                response = client.chat.completions.create(
                    model="gpt-4.1",
                    messages=[
                        {"role": "system", "content": "あなたはSNS運用のプロです。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.9
                )
                output = response.choices[0].message.content.strip()
                st.success("✨ 投稿案が完成しました！")
                st.markdown("**【投稿ネタ】**")
                st.markdown(f"{topic}")
                st.markdown("**【ターゲット】**")
                st.markdown(f"{target}")
                st.markdown("**【目的】**")
                st.markdown(f"{purpose}")
                st.markdown("**【投稿形式】**")
                st.markdown(f"{format_type}")
                st.markdown("---")
                st.markdown(output)

                st.session_state["post_output"] = {
                    "topic": topic,
                    "target": target,
                    "purpose": purpose,
                    "format": format_type,
                    "output": output
                }
                
                # --- ページ切り替え方式に対応した投稿登録リンク ---
                current_url = st.get_page_config().get("url", "") if hasattr(st, "get_page_config") else ""
                query = urllib.parse.urlencode({"page": "投稿登録"})
                register_url = f"{current_url}?{query}" if current_url else "?page=投稿登録"

                st.markdown(f"📥 投稿登録はこちら 👉 [登録ページを開く]({register_url})")
                
            except Exception as e:
                st.error(f"投稿案生成中にエラーが発生しました：{e}")
                
                
