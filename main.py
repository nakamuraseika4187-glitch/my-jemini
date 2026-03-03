import streamlit as st
from google import genai
from PIL import Image
import os

# --- 設定 ---
st.set_page_config(page_title="伝票解析アシスタント", layout="wide")
st.title("📝 伝票解析＆チャットAI")

# APIキーの設定（Secretsから読み込み）
MY_API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=MY_API_KEY)

# --- 会話履歴の保存（これがないと会話を忘れてしまいます） ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- サイドバー：写真のアップロード ---
with st.sidebar:
    st.header("1. 伝票の読み込み")
    uploaded_file = st.file_uploader("写真をアップロード", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption='現在の伝票', use_container_width=True)
        
        if st.button("この伝票を解析して会話を始める"):
            # 最初の解析
            with st.spinner("解析中..."):
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=["この伝票を詳細に文字起こしして整理してください。", image]
                )
                # 最初の返答を履歴に追加
                st.session_state.messages.append({"role": "assistant", "content": response.text})

    if st.button("会話をリセット"):
        st.session_state.messages = []
        st.rerun()

# --- メイン画面：チャット機能 ---
st.subheader("2. AIと対話する")

# 過去のメッセージを表示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ユーザーの入力を受け付ける
if prompt := st.chat_input("この伝票について質問してください（例：合計金額は？）"):
    # ユーザーのメッセージを表示
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # AIの返答を生成
    with st.chat_message("assistant"):
        with st.spinner("考え中..."):
            # 画像がある場合は画像も一緒に送る
            input_content = [prompt]
            if uploaded_file:
                input_content.append(image)
            
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=input_content
            )
            st.write(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
