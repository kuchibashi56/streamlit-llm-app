# 環境変数の読み込み
from dotenv import load_dotenv

load_dotenv()

# Streamlitの設定、および説明文の表示
import streamlit as st

st.title("専門家チャットアプリ")

st.write("##### モード1: ヘルスケア")
st.write("健康に関する質問に対して、専門的な回答を提供します。")
st.write("##### モード2: ビジネス")
st.write("ビジネスに関する質問に対して、専門的な回答を提供します。")

# 動作モードの選択肢をラジオボタンで表示
st.divider() # 区切り線を引く
selected_item = st.radio(
    "動作モードを選択してください。",
    ["ヘルスケア", "ビジネス"]
)

# チャット履歴を表示
if "chat_history" in st.session_state and st.session_state["chat_history"]:
    st.write("#### チャット履歴")
    for msg in st.session_state["chat_history"]:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        elif msg["role"] == "ai":
            st.markdown(f"**AI:** {msg['content']}")

st.divider() # 区切り線を引く

if selected_item == "ヘルスケア":
    input_message = st.text_input(label="健康に関する質問を入力してください。", key="input_message")
elif selected_item == "ビジネス":
    input_message = st.text_input(label="ビジネスに関する質問を入力してください。", key="input_message")

# LLMのインポート、およびチャットロジックの実装
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage

def get_llm_response(input_message: str, selected_item: str, chat_history: list) -> str:
    if selected_item == "ヘルスケア":
        system_prompt = "You will answer questions as a health expert. You must answer in Japanese."
    elif selected_item == "ビジネス":
        system_prompt = "You will answer questions as a business expert. You must answer in Japanese."
    else:
        return "不明なモードです。"

    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    messages = [SystemMessage(content=system_prompt)]
    # chat_historyからHumanMessage, AIMessageを復元
    for msg in chat_history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "ai":
            messages.append(AIMessage(content=msg["content"]))
    # 今回のユーザー入力を追加
    messages.append(HumanMessage(content=input_message))
    result = llm.invoke(messages)
    return result.content

if st.button("実行"):
    st.divider()

    if input_message:
        response = get_llm_response(input_message, selected_item, st.session_state["chat_history"])
        st.session_state["chat_history"].append({"role": "user", "content": input_message})
        st.session_state["chat_history"].append({"role": "ai", "content": response})
    else:
        st.error(f"{selected_item}の質問を入力してから「実行」ボタンを押してください。")

# チャット履歴を表示
if st.session_state["chat_history"]:
    st.write("#### チャット履歴")
    for msg in st.session_state["chat_history"]:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        elif msg["role"] == "ai":
            st.markdown(f"**AI:** {msg['content']}")