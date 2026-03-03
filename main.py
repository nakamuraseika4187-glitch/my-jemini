import streamlit as st
from google import genai
import os

st.title("🚀 復旧テストモード")

# 1. 鍵のチェック
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Secretsに 'GEMINI_API_KEY' が見つかりません。")
    st.stop()

# 2. 接続の準備
try:
    api_key = st.secrets["GEMINI_API_KEY"].strip()
    client = genai.Client(api_key=api_key)
    
    # 3. チャット
    if prompt := st.chat_input("テストメッセージを送ってください"):
        with st.chat_message("user"):
            st.write(prompt)
            
        with st.chat_message("assistant"):
            # ここでモデル名を「安定版」に固定してテストします
            response = client.models.generate_content(
                model="gemini-1.5-flash", 
                contents=prompt
            )
            st.write(response.text)

except Exception as e:
    # 詳しいエラー内容を画面に出すようにしました
    st.error("エラーが発生しました。内容を確認してください。")
    st.code(str(e)) # これでエラーの正体がわかります
