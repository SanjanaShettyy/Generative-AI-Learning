import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

st.set_page_config(page_title="Mood Swing AI", page_icon="🎭")
st.title("🎭 Mood Swing AI")

# Initialize model once
if "model" not in st.session_state:
    st.session_state.model = ChatMistralAI(
        model="mistral-small-2506",
        temperature=0.9
    )

if "mode_selected" not in st.session_state:
    st.session_state.mode_selected = False

if "messages" not in st.session_state:
    st.session_state.messages = []

if "stopped" not in st.session_state:
    st.session_state.stopped = False

# Mode selection screen (equivalent to the choice = int(input(...)) step)
if not st.session_state.mode_selected:
    st.subheader("Choose your AI Mode")
    choice = st.radio(
        "Tell your response:",
        options=[1, 2, 3],
        format_func=lambda x: {1: "Angry Mode", 2: "Funny Mode", 3: "Sad Mode"}[x]
    )

    if st.button("Start Chat"):
        if choice == 1:
            mode = "You are an Amgry AI Agent. You respond aggressively and impatiently."
        elif choice == 2:
            mode = "You are a funny AI Agent. You respond with humor and jokes"
        elif choice == 3:
            mode = "You are a Sad AI Agent. You respond in a sad manner."

        st.session_state.messages = [SystemMessage(content=mode)]
        st.session_state.mode_selected = True
        st.rerun()

else:
    st.caption("------Welcome type 0 to exit the application------")

    for msg in st.session_state.messages:
        if isinstance(msg, HumanMessage):
            with st.chat_message("user"):
                st.write(msg.content)
        elif isinstance(msg, AIMessage):
            with st.chat_message("assistant"):
                st.write(msg.content)

    if st.session_state.stopped:
        st.info("Application exited. Refresh the page to start again.")
    else:
        prompt = st.chat_input("You:")

        if prompt is not None:
            st.session_state.messages.append(HumanMessage(content=prompt))

            with st.chat_message("user"):
                st.write(prompt)

            if prompt == "0":
                st.session_state.stopped = True
                st.rerun()
            else:
                response = st.session_state.model.invoke(st.session_state.messages)
                st.session_state.messages.append(AIMessage(content=response.content))

                with st.chat_message("assistant"):
                    st.write(response.content)