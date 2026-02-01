import os
from dotenv import load_dotenv
load_dotenv()

# 入力フォームを用意する
import streamlit as st
st.title("スポーツ相談窓口")
user_input = st.text_area("スポーツに関する質問をどうぞ！", height=200)

# OpenAI APIキーの取得（環境変数 or Streamlit CloudのSecrets）
api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
if not api_key:
    st.error("OPENAI_API_KEY が設定されていません。Secrets または .env に設定してください。")
else:
    os.environ["OPENAI_API_KEY"] = api_key

# LangChainの新しいパッケージ構成に合わせたインポート
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)

# user_inputのテキストをLLMに渡し、回答結果を表示する
if st.button("相談する"):
    if user_input.strip() == "":
        st.warning("質問を入力してください。")
    else:
        with st.spinner("回答を生成中..."):
            response = llm.invoke(user_input)
        st.subheader("回答:")
        st.write(response.content)

# ラジオボタンでLLMに振舞わせる専門家の種類を選択する。専門家はサッカー、野球、バスケットボール、テニス、陸上競技から選べるようにする
expertise = st.radio("専門家の種類を選んでください:",
                     ("サッカー", "野球", "バスケットボール", "テニス", "陸上競技"))
st.write(f"選択された専門家: {expertise}") 

# 選択された専門家の種類に基づいて、プロンプトをカスタマイズする
if st.button("専門家に相談する"):
    if user_input.strip() == "":
        st.warning("質問を入力してください。")
    else:
        customized_prompt = f"あなたは{expertise}の専門家です。以下の質問に答えてください:\n{user_input}"
        with st.spinner("回答を生成中..."):
            response = llm.invoke(customized_prompt)
        st.subheader("専門家からの回答:")
        st.write(response.content)

# ページのサイドバーにアプリの説明を追加する
st.sidebar.title("アプリの説明")
st.sidebar.info(
    """
    このアプリはスポーツに関する質問に答えるための相談窓口です。質問を入力し、専門家の種類を選択して「相談する」ボタンを押すと、AIが回答を生成します。専門家の種類にはサッカー、野球、バスケットボール、テニス、陸上競技があります。ぜひお気軽にご利用ください！
    """
)
