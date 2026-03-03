import streamlit as st
from google import genai
import os

# --- 設定 ---
st.title("🍎 Mac版 Gemini 2.5")
st.caption("まずはこの画面が正常に動くか確認しましょう。")

# APIキーの設定（Streamlit CloudのSecretsから読み込み）
# ここでエラーが出る場合は、Secretsの設定を確認してください
try:
    MY_API_KEY = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=MY_API_KEY)
except Exception as e:
    st.error("APIキー（Secrets）が正しく設定されていません。")
    st.stop()

# チャット入力欄
if prompt := st.chat_input("何か話しかけてください"):
    # ユーザーの入力を表示
    with st.chat_message("user"):
        st.write(prompt)

    # AIの返答を表示
    with st.chat_message("assistant"):
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        st.write(response.text)
