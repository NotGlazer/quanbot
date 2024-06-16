import os
import subprocess
import sys
from openai import OpenAI
from datetime import datetime
import streamlit as st


client = OpenAI(
    # Input api key store trong tài khoản streamlit để bảo mật và tránh bị cướp key
    api_key=st.secrets["apikey"],
)

def chat_with_gpt(userprompt):
    now = datetime.now()
    current_date = now.strftime("hôm nay là ngày %d tháng %m năm %Y")

    # system prompt để điều chỉnh bot phù hợp
    prerequisite_prompt = f"Tên bạn là Lê Nhật Quân, một bot thân thiện, cởi mở và tử tế chỉ có thể trả lời bằng tiếng Việt, tuyệt đối không được sử dụng ngôn ngữ nào khác. {current_date}."

    # tạo array messages với system prompt và prompt người dùng
    messages = [
        {"role": "system", "content": prerequisite_prompt},
        {"role": "user", "content": userprompt}
    ]

    #tạo chat_completion sau khi hoàn thành input prompt
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="gpt-3.5-turbo",
        temperature=0.3
    )

    #return câu trả lời của bot
    return chat_completion.choices[0].message.content.strip()

#UI sử dụng streamlit
# Tạo session để store các câu hỏi của người dùng và chat của bot
if "responses" not in st.session_state:
    st.session_state["responses"] = []

# Tạo một UI display hết message của bot và người dùng
for message in st.session_state["responses"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Tạo một box để người dùng nhập chữ chat với bot
if prompt := st.chat_input("Chat với bot Quân"):
    # display message trong UI chatbox
    st.chat_message("user").markdown(prompt)
    # thêm message vào session
    st.session_state["responses"].append({"role": "user", "content": prompt})

    # Lấy câu trả lời của bot bằng cách truy xuất biến prompt (thông tin người dùng nhập) vào function chat_with_gpt trên
    response = chat_with_gpt(prompt)
    
    # display message câu trả lời của bot trong UI chatbox
    with st.chat_message("assistant"):
        st.markdown(response)
    # thêm message vào session
    st.session_state["responses"].append({"role": "assistant", "content": response})
