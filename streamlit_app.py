import streamlit as st
from datetime import datetime
import pandas as pd
import os
import time
from twilio.rest import Client
import requests

# 共享聊天记录文件名
CHAT_FILE = "chat_history.csv"

# 密码配置
CORRECT_PASSWORD = "hello world"  # 设置你的密码

# Twilio配置（请替换为你自己的凭据）
ACCOUNT_SID = "AC6d70171e378d8da26ee5521c78214382"
AUTH_TOKEN = "39af64209304f3a8b82b83b10ca899c4"
TWILIO_PHONE = "+13412182075"
TO_PHONE = "+8615616139621"

# Server酱配置
SERVER_CHAN_URL = "https://sctapi.ftqq.com/SCT31129TtqguxCLA1OYNhAf1mtxxmyz3.send"

# 设置页面标题和图标
st.set_page_config(
    page_title="NEON-CHAT 2119", 
    page_icon="💬",
    layout="wide"
)

# 应用赛博朋克CSS样式
def set_cyberpunk_style():
    st.markdown("""
    <style>
    :root {
        --primary-color: #ff2a6d;
        --secondary-color: #05d9e8;
        --bg-color: #0d0221;
        --text-color: #d1f7ff;
        --accent-color: #005678;
        --neon-glow: 0 0 10px var(--primary-color), 0 0 20px var(--secondary-color);
    }
    
    body {
        background-color: var(--bg-color);
        color: var(--text-color);
        font-family: 'Courier New', monospace;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0d0221 0%, #1a1b3a 100%);
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: var(--primary-color);
        text-shadow: 0 0 5px var(--primary-color), 0 0 10px var(--primary-color);
    }
    
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: rgba(13, 2, 33, 0.7);
        color: var(--secondary-color);
        border: 1px solid var(--primary-color);
        border-radius: 0;
    }
    
    .stButton>button {
        background-color: var(--accent-color);
        color: var(--secondary-color);
        border: 1px solid var(--primary-color);
        border-radius: 0;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background-color: var(--primary-color);
        color: white;
        box-shadow: 0 0 10px var(--primary-color), 0 0 20px var(--primary-color);
    }
    
    .stChatMessage {
        background-color: rgba(5, 217, 232, 0.1) !important;
        border-left: 3px solid var(--primary-color) !important;
        margin: 10px 0;
        padding: 10px;
    }
    
    .stSidebar {
        background: linear-gradient(180deg, #0d0221 0%, #1a1b3a 100%) !important;
        border-right: 1px solid var(--primary-color) !important;
    }
    
    .stAlert {
        background-color: rgba(255, 42, 109, 0.2) !important;
        border-left: 3px solid var(--primary-color) !important;
    }
    
    .stSuccess {
        background-color: rgba(5, 217, 232, 0.2) !important;
        border-left: 3px solid var(--secondary-color) !important;
    }
    
    .stMarkdown {
        color: var(--text-color);
    }
    
    /* 自定义霓虹边框 */
    .neon-box {
        border: 1px solid var(--primary-color);
        box-shadow: 0 0 10px var(--primary-color), 0 0 20px var(--primary-color);
        padding: 15px;
        margin: 10px 0;
        position: relative;
    }
    
    .neon-box::before {
        content: "";
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        border: 1px solid var(--secondary-color);
        box-shadow: 0 0 10px var(--secondary-color), 0 0 20px var(--secondary-color);
        z-index: -1;
    }
    
    /* 终端效果 */
    .terminal {
        background-color: rgba(0, 0, 0, 0.7);
        border: 1px solid var(--secondary-color);
        padding: 15px;
        font-family: 'Courier New', monospace;
        color: var(--secondary-color);
        position: relative;
    }
    
    .terminal::before {
        content: "> ";
        position: absolute;
        left: 5px;
        top: 15px;
    }
    
    /* 扫描线效果 */
    body::after {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(
            rgba(18, 16, 16, 0) 50%, 
            rgba(0, 0, 0, 0.25) 50%
        );
        background-size: 100% 4px;
        z-index: 9999;
        pointer-events: none;
        animation: scanline 6s linear infinite;
    }
    
    @keyframes scanline {
        0% {
            background-position: 0 0;
        }
        100% {
            background-position: 0 100%;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# 检查密码
def check_password():
    """返回是否通过密码验证"""
    if 'password_correct' not in st.session_state:
        st.session_state.password_correct = False
    
    if st.session_state.password_correct:
        return True
    
    # 赛博朋克风格的登录界面
    st.markdown("""
    <div style="text-align: center; margin-top: 100px;">
        <h1 style="color: #ff2a6d; text-shadow: 0 0 10px #ff2a6d, 0 0 20px #ff2a6d;">WELCOME TO 2119</h1>
        <p style="color: #05d9e8; font-size: 1.2em;">NEURAL INTERFACE TERMINAL</p>
        <div style="margin: 50px auto; width: 300px; border: 1px solid #ff2a6d; 
            box-shadow: 0 0 15px #ff2a6d, 0 0 30px #05d9e8; padding: 30px;">
    """, unsafe_allow_html=True)
    
    # 密码输入表单
    with st.form("密码验证"):
        password = st.text_input("ENTER ACCESS CODE", type="password", 
                               help="Authorization required for neural uplink")
        submitted = st.form_submit_button("AUTHENTICATE")
        
        if submitted:
            if password == CORRECT_PASSWORD:
                st.session_state.password_correct = True
                st.success("ACCESS GRANTED. INITIALIZING NEURAL INTERFACE...")
                time.sleep(1)  # 给用户看到成功消息
                st.rerun()
            else:
                st.error("UNAUTHORIZED ACCESS DETECTED. SYSTEM LOCKDOWN INITIATED.")
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    return False

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
        st.success(f"NEURAL CALL INITIATED! CALL SID: {call.sid}")
    except Exception as e:
        st.error(f"CALL FAILED: {str(e)}")

# 发送Server酱消息
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

# 主应用
def main_app():
    # 设置赛博朋克样式
    set_cyberpunk_style()
    
    # 侧边栏 - 用户设置
    with st.sidebar:
        st.markdown("""
        <div style="border-bottom: 1px solid #ff2a6d; padding-bottom: 10px; margin-bottom: 20px;">
            <h2 style="color: #05d9e8;">SYSTEM CONTROL PANEL</h2>
        </div>
        """, unsafe_allow_html=True)

        # 用户名输入
        if 'user_name' not in st.session_state:
            st.session_state.user_name = ""

        new_name = st.text_input("USER IDENTITY", value=st.session_state.user_name)
        if new_name != st.session_state.user_name:
            if new_name.strip():
                st.session_state.user_name = new_name.strip()
                st.success(f"IDENTITY CONFIRMED: {new_name}")
            else:
                st.warning("IDENTITY REQUIRED FOR NEURAL UPLINK")

        # 清空聊天记录按钮
        if st.button("PURGE MEMORY BANKS", key="clear_chat"):
            clear_messages()
            st.success("MEMORY PURGE COMPLETE")
        
        st.markdown("""
        <div style="border-top: 1px solid #ff2a6d; margin: 20px 0; padding-top: 10px;">
            <h3 style="color: #05d9e8;">COMMUNICATION MODULES</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # 电话呼叫部分
        if st.button("INITIATE NEURAL CALL", key="call_button"):
            make_phone_call()
        
        # Server酱消息发送部分
        with st.form("serverchan_form"):
            st.markdown("<h4 style='color: #ff2a6d;'>NEURAL MESSAGE TRANSMITTER</h4>", unsafe_allow_html=True)
            title = st.text_input("MESSAGE HEADER", value="SYSTEM ALERT")
            message = st.text_area("MESSAGE CONTENT")
            submitted = st.form_submit_button("TRANSMIT")
            
            if submitted:
                if not message:
                    st.warning("MESSAGE CONTENT REQUIRED")
                else:
                    success, result = send_serverchan_message(title, message)
                    if success:
                        st.success("MESSAGE TRANSMISSION SUCCESSFUL")
                        st.json(result)
                    else:
                        st.error(f"TRANSMISSION FAILED: {result}")

    # 主页面标题
    st.markdown("""
    <div style="display: flex; align-items: center; margin-bottom: 20px;">
        <h1 style="color: #ff2a6d; margin-right: 15px;">NEON-CHAT 2119</h1>
        <span style="color: #05d9e8; font-size: 0.8em; margin-top: 10px;">NEURAL INTERFACE ONLINE</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='color: #05d9e8; margin-bottom: 20px;'>MULTI-USER NEURAL LINK ESTABLISHED</div>", unsafe_allow_html=True)

    # 显示聊天记录
    messages = load_messages()
    for _, row in messages.iterrows():
        if pd.notna(row['user']) and str(row['user']).strip():
            with st.chat_message(name=str(row['user']).strip()):
                st.markdown(f"""
                <div style="color: #d1f7ff;">
                    <span style="color: #ff2a6d; font-weight: bold;">{row['user']}</span> 
                    <span style="color: #05d9e8; font-size: 0.8em;">[{row['timestamp']}]</span>: 
                    {row['message']}
                </div>
                """, unsafe_allow_html=True)

    # 输入新消息
    if prompt := st.chat_input("INPUT MESSAGE..."):
        if not st.session_state.user_name or not st.session_state.user_name.strip():
            st.warning("IDENTITY VERIFICATION REQUIRED - PLEASE SET USER IDENTITY")
            st.stop()

        # 保存消息
        save_message(st.session_state.user_name, prompt)

        # 显示自己的消息
        with st.chat_message(name=st.session_state.user_name):
            st.markdown(f"""
            <div style="color: #d1f7ff;">
                <span style="color: #ff2a6d; font-weight: bold;">{st.session_state.user_name}</span> 
                <span style="color: #05d9e8; font-size: 0.8em;">[{datetime.now().strftime('%H:%M:%S')}]</span>: 
                {prompt}
            </div>
            """, unsafe_allow_html=True)

        st.rerun()

    # 每5秒自动刷新页面以获取他人消息
    time.sleep(5)
    st.rerun()

# 应用入口
if not check_password():
    st.stop()

main_app()
