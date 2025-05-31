import streamlit as st
from datetime import datetime
import time

# 设置页面标题
st.set_page_config(page_title="极简聊天室", page_icon="💬")

# 全局存储聊天记录（所有用户共享）
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 用户设置
if "user_name" not in st.session_state:
    st.session_state.user_name = st.text_input("请输入你的名字", key="username_input")
    if st.session_state.user_name:
        st.success(f"欢迎, {st.session_state.user_name}!")
    st.stop()  # 必须设置名字才能继续

# 显示所有聊天记录
for msg in st.session_state.chat_history:
    with st.chat_message(name=msg["user"]):
        st.write(f"**{msg['user']}** ({msg['time']}): {msg['text']}")

# 输入新消息
if new_msg := st.chat_input("输入消息..."):
    # 添加到全局聊天记录
    st.session_state.chat_history.append({
        "user": st.session_state.user_name,
        "time": datetime.now().strftime("%H:%M:%S"),
        "text": new_msg
    })
    # 显示新消息
    with st.chat_message(name=st.session_state.user_name):
        st.write(f"**{st.session_state.user_name}** ({datetime.now().strftime('%H:%M:%S')}): {new_msg}")
    
    # 自动刷新（模拟"实时"效果）
    time.sleep(0.1)
    st.rerun()

# 每2秒自动刷新（获取新消息）
time.sleep(2)
st.rerun()
