import streamlit as st
from google import genai
from PIL import Image
import os

# タイトルと説明
st.title("📝 伝票文字起こしAI")
st.caption("手書き伝票の写真をアップロードすると、テキストに変換します。")

# APIキーの設定（Streamlit CloudのSecretsから読み込み）
MY_API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=MY_API_KEY)

# 1. 写真をアップロードする機能
uploaded_file = st.file_uploader("伝票の写真をアップロードしてください", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    # アップロードされた画像を表示
    image = Image.open(uploaded_file)
    st.image(image, caption='アップロードされた画像', use_container_width=True)

    # 2. 実行ボタン
    if st.button('文字起こしを開始する'):
        with st.spinner('手書き文字を解析中...'):
            try:
                # Geminiに画像を渡して「文字起こしして」と頼む
                response = client.models.generate_content(
                    model="gemini-2.0-flash", # 最新の高速モデル
                    contents=[
                        "この伝票の画像を読み取り、項目（日付、品名、金額など）を整理してテキストで出力してください。",
                        image
                    ]
                )
                
                # 結果を表示
                st.success('文字起こしが完了しました！')
                st.markdown("### 解析結果")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")

else:
    st.info("左上のボタンから画像を選んでください。")
