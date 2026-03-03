import streamlit as st
from google import genai
import os

# Macの文字コード問題を力技で解決する設定
os.environ["LANG"] = "ja_JP.UTF-8"
os.environ["LC_ALL"] = "ja_JP.UTF-8"

st.title("🍎 Mac版 Gemini 2.5")

# --- 修正ポイント：APIキーを画面から入力させる ---
# これにより、プログラム内部での文字変換エラーを回避できる可能性が高まります
api_key_input = st.text_input("Gemini APIキーを入力してください", type="password")

if api_key_input:
    # 前後の空白を削除
    client = genai.Client(api_key=api_key_input.strip())
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("何か聞いてみて！"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash", 
                    contents=prompt
                )
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
else:
    st.info("APIキーを入力するとチャットが始まります。")