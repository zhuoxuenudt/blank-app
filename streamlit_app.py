import streamlit as st
from datetime import datetime
import pandas as pd
import time

# 设置页面标题和图标
st.set_page_config(page_title="实时聊天室", page_icon="💬")

# 使用session_state存储聊天记录和用户信息
if 'messages' not in st.session_state:
    st.session_state.messages = pd.DataFrame(columns=['timestamp', 'user', 'message'])

if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

# 侧边栏 - 用户设置
with st.sidebar:
    st.title("聊天室设置")
    
    # 用户名输入
    new_name = st.text_input("你的名字", value=st.session_state.user_name)
    if new_name != st.session_state.user_name:
        st.session_state.user_name = new_name
        st.success(f"已设置用户名: {new_name}")
    
    # 清空聊天记录按钮
    if st.button("清空聊天记录"):
        st.session_state.messages = pd.DataFrame(columns=['timestamp', 'user', 'message'])
        st.success("已清空聊天记录")

# 主页面标题
st.title("💬 实时聊天室")
st.caption("多人可以同时在不同设备上聊天")

# 显示聊天记录
for _, row in st.session_state.messages.iterrows():
    with st.chat_message(name=row['user']):
        st.write(f"**{row['user']}** ({row['timestamp']}): {row['message']}")

# 输入新消息
if prompt := st.chat_input("输入消息..."):
    if not st.session_state.user_name:
        st.warning("请先在侧边栏设置你的名字")
        st.stop()
    
    # 添加新消息到聊天记录
    new_message = {
        'timestamp': datetime.now().strftime("%H:%M:%S"),
        'user': st.session_state.user_name,
        'message': prompt
    }
    st.session_state.messages.loc[len(st.session_state.messages)] = new_message
    
    # 显示新消息
    with st.chat_message(name=st.session_state.user_name):
        st.write(f"**{st.session_state.user_name}** ({new_message['timestamp']}): {prompt}")
    
    # 自动刷新页面以显示其他人的消息
    st.rerun()

# 每5秒自动刷新页面以获取新消息
time.sleep(5)
st.rerun()
