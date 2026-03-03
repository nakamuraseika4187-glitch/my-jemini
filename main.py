import streamlit as st
from google import genai
from PIL import Image
import io

# --- 設定 ---
st.set_page_config(page_title="伝票解析アシスタント", layout="wide")
st.title("📝 伝票解析＆チャットAI")

# APIキーの設定
MY_API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=MY_API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- サイドバー ---
with st.sidebar:
    st.header("1. 伝票の読み込み")
    uploaded_file = st.file_uploader("写真をアップロード", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file:
        # 画面表示用の画像
        image = Image.open(uploaded_file)
        st.image(image, caption='現在の伝票', use_container_width=True)
        
        if st.button("この伝票を解析して会話を始める"):
            with st.spinner("解析中..."):
                # 【重要】エラー回避：画像をバイトデータとして抽出
                img_bytes = uploaded_file.getvalue()
                
                # Geminiに画像と指示を送る
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=[
                        "この伝票を詳細に文字起こしして整理してください。日本語で回答してください。",
                        {"mime_type": "image/jpeg", "data": img_bytes}
                    ]
                )
                st.session_state.messages.append({"role": "assistant", "content": response.text})

    if st.button("会話をリセット"):
        st.session_state.messages = []
        st.rerun()

# --- メイン画面 ---
st.subheader("2. AIと対話する")

# 過去の履歴を表示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# チャット入力
if prompt := st.chat_input("質問してください（例：合計金額は？）"):
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("考え中..."):
            # 送信内容のリストを作成
            input_content = [prompt]
            
            if uploaded_file:
                # 【重要】チャット時も画像をデータとして追加
                img_bytes = uploaded_file.getvalue()
                input_content.append({"mime_type": "image/jpeg", "data": img_bytes})
            
            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=input_content
                )
                st.write(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error("通信中にエラーが発生しました。")
                st.info(f"技術的なエラー詳細: {e}")
