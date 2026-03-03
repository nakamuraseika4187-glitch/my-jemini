import streamlit as st
from google import genai

st.title("🚀 最終接続テスト")

# Secretsのチェック
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Secretsに 'GEMINI_API_KEY' が設定されていません。")
    st.stop()

try:
    # 接続準備
    api_key = st.secrets["GEMINI_API_KEY"].strip().replace('"', '') # 引用符を掃除
    client = genai.Client(api_key=api_key)
    
    if prompt := st.chat_input("何か入力してください"):
        with st.chat_message("user"):
            st.write(prompt)
            
        with st.chat_message("assistant"):
            # 【ここを修正】モデル名から 'models/' を外して指定します
            response = client.models.generate_content(
                model="gemini-2.0-flash", 
                contents=prompt
            )
            st.write(response.text)

except Exception as e:
    st.error("エラーが発生しました。")
    st.code(str(e))
