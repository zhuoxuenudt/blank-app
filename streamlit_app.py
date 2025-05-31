import streamlit as st
from datetime import datetime
import pandas as pd
import os
import time
from twilio.rest import Client

# 共享聊天记录文件名
CHAT_FILE = "chat_history.csv"

# Twilio配置（请替换为你自己的凭据）
ACCOUNT_SID = "USd66bbf7121ea9681d24b70adfd1435c5"  # 替换为你的 ACCOUNT_SID
AUTH_TOKEN = "aaaf081550bce701b610661da8b5e71f"    # 替换为你的 AUTH_TOKEN
TWILIO_PHONE = "+13412182075"      # 替换为你的 Twilio 电话号码
TO_PHONE = "+8615616139621"         # 替换为目标电话号码（带国际区号）

# 设置页面标题和图标
st.set_page_config(page_title="实时聊天室", page_icon="💬")

# 初始化聊天记录文件（如果不存在）
if not os.path.exists(CHAT_FILE):
    pd.DataFrame(columns=['timestamp', 'user', 'message']).to_csv(CHAT_FILE, index=False)

# 加载聊天记录
def load_messages():
    return pd.read_csv(CHAT_FILE)

# 保存新消息到聊天记录
def save_message(user, message):
    if not user or not message:  # 确保用户名和消息都不为空
        return
    new_message = pd.DataFrame([{
        'timestamp': datetime.now().strftime("%H:%M:%S"),
        'user': user.strip(),  # 去除前后空格
        'message': message
    }])
    new_message.to_csv(CHAT_FILE, mode='a', index=False, header=False)

# 清空聊天记录
def clear_messages():
    pd.DataFrame(columns=['timestamp', 'user', 'message']).to_csv(CHAT_FILE, index=False)

# 发起电话呼叫
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

# 侧边栏 - 用户设置
with st.sidebar:
    st.title("聊天室设置")

    # 用户名输入
    if 'user_name' not in st.session_state:
        st.session_state.user_name = ""

    new_name = st.text_input("你的名字", value=st.session_state.user_name)
    if new_name != st.session_state.user_name:
        if new_name.strip():  # 确保用户名不为空
            st.session_state.user_name = new_name.strip()
            st.success(f"已设置用户名: {new_name}")
        else:
            st.warning("用户名不能为空")

    # 清空聊天记录按钮
    if st.button("清空聊天记录"):
        clear_messages()
        st.success("已清空聊天记录")
    
    # 分隔线
    st.divider()
    
    # 电话呼叫部分
    st.title("电话呼叫功能")
    if st.button("发起电话呼叫", key="call_button"):
        make_phone_call()

# 主页面标题
st.title("💬 实时聊天室")
st.caption("支持多人同时聊天 - 使用共享CSV实现同步")

# 显示聊天记录
messages = load_messages()
for _, row in messages.iterrows():
    # 确保用户名不为空
    if pd.notna(row['user']) and str(row['user']).strip():
        with st.chat_message(name=str(row['user']).strip()):
            st.write(f"**{row['user']}** ({row['timestamp']}): {row['message']}")

# 输入新消息
if prompt := st.chat_input("输入消息..."):
    if not st.session_state.user_name or not st.session_state.user_name.strip():
        st.warning("请先在侧边栏设置你的名字")
        st.stop()

    # 保存消息
    save_message(st.session_state.user_name, prompt)

    # 显示自己的消息
    with st.chat_message(name=st.session_state.user_name):
        st.write(f"**{st.session_state.user_name}** ({datetime.now().strftime('%H:%M:%S')}): {prompt}")

    st.rerun()

# 每5秒自动刷新页面以获取他人消息
time.sleep(5)
st.rerun()
