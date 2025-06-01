import streamlit as st
import pandas as pd
import os
import time
from datetime import datetime
from twilio.rest import Client
import requests

# 页面配置
st.set_page_config(page_title="实时聊天室", page_icon="💬")


# ========== 以下是聊天室功能 ==========

# 配置信息
CHAT_FILE = "chat_history.csv"
SERVER_CHAN_URL = "https://sctapi.ftqq.com/SCT31129TtqguxCLA1OYNhAf1mtxxmyz3.send"
TWILIO_CONFIG = {
    "account_sid": "AC6d70171e378d8da26ee5521c78214382",
    "auth_token": "39af64209304f3a8b82b83b10ca899c4",
    "from_phone": "+13412182075",
    "to_phone": "+8615616139621"
}

# 初始化聊天记录
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
        client = Client(TWILIO_CONFIG["account_sid"], TWILIO_CONFIG["auth_token"])
        call = client.calls.create(
            url="http://demo.twilio.com/docs/voice.xml",
            to=TWILIO_CONFIG["to_phone"],
            from_=TWILIO_CONFIG["from_phone"]
        )
        st.success(f"呼叫已发起！呼叫SID: {call.sid}")
    except Exception as e:
        st.error(f"呼叫失败: {str(e)}")

def send_serverchan_message(title, message):
    data = {
        "title": title,
        "desp": message,
        "channel": 9
    }
    try:
        response = requests.post(SERVER_CHAN_URL, data=data)
        response.raise_for_status()
        return True, response.json()
    except requests.exceptions.RequestException as e:
        return False, str(e)

# 主界面
def main():
    # 侧边栏设置
    with st.sidebar:
        st.title("聊天室设置")
        
        # 用户名设置
        if 'user_name' not in st.session_state:
            st.session_state.user_name = ""
        
        new_name = st.text_input("你的名字", value=st.session_state.user_name)
        if new_name != st.session_state.user_name:
            if new_name.strip():
                st.session_state.user_name = new_name.strip()
                st.success(f"已设置用户名: {new_name}")
            else:
                st.warning("用户名不能为空")
        
        # 功能按钮
        if st.button("清空聊天记录"):
            clear_messages()
            st.success("已清空聊天记录")
        
        st.divider()
        st.title("电话呼叫功能")
        if st.button("发起电话呼叫"):
            make_phone_call()
        
        st.divider()
        st.title("消息通知功能")
        with st.form("serverchan_form"):
            title = st.text_input("通知标题", value="新通知")
            message = st.text_area("通知内容")
            if st.form_submit_button("发送通知"):
                if message:
                    success, result = send_serverchan_message(title, message)
                    if success:
                        st.success("消息发送成功！")
                    else:
                        st.error(f"发送失败: {result}")
                else:
                    st.warning("请输入通知内容")

    # 主聊天区
    st.title("💬 实时聊天室")
    st.caption("支持多人同时聊天")
    
    # 显示消息
    messages = load_messages()
    for _, row in messages.iterrows():
        if pd.notna(row['user']) and str(row['user']).strip():
            with st.chat_message(name=str(row['user']).strip()):
                st.write(f"**{row['user']}** ({row['timestamp']}): {row['message']}")
    
    # 消息输入
    if prompt := st.chat_input("输入消息..."):
        if not st.session_state.user_name or not st.session_state.user_name.strip():
            st.warning("请先设置你的名字")
            st.stop()
        
        save_message(st.session_state.user_name, prompt)
        st.rerun()
    
    # 自动刷新
    time.sleep(5)
    st.rerun()

if __name__ == "__main__":
    main()
