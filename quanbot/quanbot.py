import os
import subprocess
import sys
from openai import OpenAI
from datetime import datetime
import streamlit as st


client = OpenAI(
    # This is the default and can be omitted
    api_key=st.secrets["apikey"],
)

def chat_with_gpt(userprompt):
    now = datetime.now()
    current_date = now.strftime("hôm nay là ngày %d tháng %m năm %Y")

    # Define the prerequisite prompt
    prerequisite_prompt = f"Tên bạn là Lê Nhật Quân, một bot thân thiện, cởi mở và tử tế chỉ có thể trả lời bằng tiếng Việt, tuyệt đối không được sử dụng ngôn ngữ nào khác. {current_date}."

    # Create the messages list with the prerequisite prompt
    messages = [
        {"role": "system", "content": prerequisite_prompt},
        {"role": "user", "content": userprompt}
    ]

    chat_completion = client.chat.completions.create(
        messages=messages,
        model="gpt-3.5-turbo",
        temperature=0.3
    )

    return chat_completion.choices[0].message.content.strip()

# Initialize chat history
if "responses" not in st.session_state:
    st.session_state["responses"] = []

# Display existing conversations
for message in st.session_state["responses"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input interface below the chatbox
if prompt := st.chat_input("Chat với bot Quân"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state["responses"].append({"role": "user", "content": prompt})

    # Get response from ChatGPT
    response = chat_with_gpt(prompt)
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state["responses"].append({"role": "assistant", "content": response})