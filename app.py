
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key
openai.api_type = "azure"
openai.api_base = st.secrets.OpenAIAPI.openai_api_base
openai.api_version = "2023-03-15-preview"

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role":"system","content":"あなたは、社内向けのファイナンスニュース紹介文書のドラフト生成をするAIアシスタントです。"},
        {"role":"user","content":"最新AIニュースの紹介文を作ってください。"},
        {"role":"assistant","content":"おはようございます\nFinTech Product Strategy Gr〇●です\n\n夢の、ドキュメント自動化が近づいています。\n\nみずほ、システム開発・保守を生成AIで改善　富士通と実証実験\nhttps://www.itmedia.co.jp/news/articles/2306/19/news149.html\n\nーーーー\n富士通は6月19日、みずほフィナンシャルグループのシステム開発・保守作業を改善する実証実験を始めたと発表した。生成AIを活用し、システム設計書の記載漏れや書き間違いを自動検出 するという。2024年3月31日まで2社共同で実施する。\n\n　設計書の記載漏れを防ぐだけでなく、修正した書類を基に、システムテストの仕様書をAIで自動生成する技術の開発 も目指す。システムの開発・保守そのものをAIに任せることが可能かの検証も進めるという。\nーーーー"}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        engine="AokiChatGPTTest20230530",
        model="gpt-3.5-turbo",
        temperature=0.0,
        messages=messages
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("Finance News Assistant")
st.write("ChatGPT APIを使ったFinance News ドラフト作成ボットです。")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
