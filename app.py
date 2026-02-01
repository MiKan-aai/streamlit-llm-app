from dotenv import load_dotenv
load_dotenv()

# 入力フォームを用意する
import streamlit as st
st.title("スポーツ相談窓口")
user_input = st.text_area("スポーツに関する質問をどうぞ！", height=200)

# user_inputのテキストをLangChainを使ってLLMにプロンプトとして渡し、回答結果を表示する
from langchain.llms import OpenAI
llm = OpenAI(temperature=0.5)
if st.button("相談する"):
    if user_input.strip() == "":
        st.warning("質問を入力してください。")
    else:
        with st.spinner("回答を生成中..."):
            response = llm(user_input)
        st.subheader("回答:")
        st.write(response)

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
            response = llm(customized_prompt)
        st.subheader("専門家からの回答:")
        st.write(response)

# ページのサイドバーにアプリの説明を追加する
st.sidebar.title("アプリの説明")
st.sidebar.info(
    """
    このアプリはスポーツに関する質問に答えるための相談窓口です。質問を入力し、専門家の種類を選択して「相談する」ボタンを押すと、AIが回答を生成します。専門家の種類にはサッカー、野球、バスケットボール、テニス、陸上競技があります。ぜひお気軽にご利用ください！
    """
)
