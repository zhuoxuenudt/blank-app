# pages/Chatroom.py
import streamlit as st
from datetime import datetime
import pandas as pd
import os
import time
from twilio.rest import Client
import requests

# 文件和配置
CHAT_FILE = "chat_history.csv"
ACCOUNT_SID = "AC6d70171e378d8da26ee5521c78214382"
AUTH_TOKEN = "39af64209304f3a8b82b83b10ca899c4"
TWILIO_PHONE = "+13412182075"
TO_PHONE = "+8615616139621"
SERVER_CHAN_URL = "https://sctapi.ftqq.com/SCT31129TtqguxCLA1OYNhAf1mtxxmyz3.send"

st.set_page_config(page_title="实时聊天室", page_icon="💬")

# 聊天记录文件初始化
if not os.path.exists(CHAT_FILE):
    pd.DataFrame(columns=['timestamp', 'user', 'message']).to_csv(CHAT_FILE, index=False)

def load_messages():
    return pd.read_csv(CHAT_FILE)

def save_message(user, message):
    if not user or not message:
        return
    new_message = pd.DataFrame([{
        'timestamp': datetime.now().strftime("%H:%M:%S"),
        'user': user.strip(),
        'message': message
    }])
    new_message.to_csv(CHAT_FILE, mode='a', index=False, header=False)

def clear_messages():
    pd.DataFrame(columns=['timestamp', 'user', 'message']).to_csv(CHAT_FILE, index=False)

def make_phone_call():
    try:
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        call = client.calls.create(
            url="http://demo.twilio.com/docs/voice.xml",
            to=TO_PHONE,
            from_=TWILIO_PHONE
        )
        st.success(f"呼叫已发起！呼叫SID: {call.sid}")
    except Exception as e:
        st.error(f"呼叫失败: {str(e)}")

def send_serverchan_message(title, message):
    data = {"title": title, "desp": message, "channel": 9}
    try:
        response = requests.post(SERVER_CHAN_URL, data=data)
        response.raise_for_status()
        return True, response.json()
    except requests.exceptions.RequestException as e:
        return False, str(e)

# 主应用界面
def main_app():
    with st.sidebar:
        st.title("聊天室设置")

        if 'user_name' not in st.session_state:
            st.session_state.user_name = ""

        new_name = st.text_input("你的名字", value=st.session_state.user_name)
        if new_name != st.session_state.user_name:
            if new_name.strip():
                st.session_state.user_name = new_name.strip()
                st.success(f"已设置用户名: {new_name}")
            else:
                st.warning("用户名不能为空")

        if st.button("清空聊天记录"):
            clear_messages()
            st.success("已清空聊天记录")

        st.divider()
        st.title("电话呼叫功能")
        if st.button("发起电话呼叫", key="call_button"):
            make_phone_call()

        st.divider()
        st.title("消息通知功能")
        with st.form("serverchan_form"):
            title = st.text_input("通知标题", value="新通知")
            message = st.text_area("通知内容")
            submitted = st.form_submit_button("发送通知")
            if submitted:
                if not message:
                    st.warning("请输入通知内容")
                else:
                    success, result = send_serverchan_message(title, message)
                    if success:
                        st.success("Server酱消息发送成功！")
                        st.json(result)
                    else:
                        st.error(f"发送失败: {result}")

    st.title("💬 实时聊天室")
    st.caption("支持多人同时聊天 - 使用共享CSV实现同步")

    messages = load_messages()
    for _, row in messages.iterrows():
        if pd.notna(row['user']) and str(row['user']).strip():
            with st.chat_message(name=str(row['user']).strip()):
                st.write(f"**{row['user']}** ({row['timestamp']}): {row['message']}")

    if prompt := st.chat_input("输入消息..."):
        if not st.session_state.user_name or not st.session_state.user_name.strip():
            st.warning("请先在侧边栏设置你的名字")
            st.stop()
        save_message(st.session_state.user_name, prompt)
        with st.chat_message(name=st.session_state.user_name):
            st.write(f"**{st.session_state.user_name}** ({datetime.now().strftime('%H:%M:%S')}): {prompt}")
        st.rerun()

    time.sleep(5)
    st.rerun()

# 启动主程序
main_app()

