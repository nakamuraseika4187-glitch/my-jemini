import sys
import io

# 日本語エラーを無理やり黙らせるおまじない
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import streamlit as st
from google import genai

st.title("🍎 再起動テスト")

try:
    # 念のため、キーから余計な空白を削除する処理を追加
    raw_key = st.secrets["GEMINI_API_KEY"]
    clean_key = raw_key.strip().replace("　", "") # 全角スペースも削除
    client = genai.Client(api_key=clean_key)
except Exception as e:
    st.error("設定画面のAPIキーを確認してください")
    st.stop()

if prompt := st.chat_input("テスト送信"):
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        st.write(response.text)
