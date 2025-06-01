import streamlit as st
from datetime import datetime
import pandas as pd
import os
import time
from twilio.rest import Client
import requests
import random
from PIL import Image
import io
import base64

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

# 卡通头像URL列表
AVATAR_URLS = [
    "https://api.dicebear.com/7.x/adventurer/svg?seed=",
    "https://api.dicebear.com/7.x/bottts/svg?seed=",
    "https://api.dicebear.com/7.x/pixel-art/svg?seed="
]

# 设置页面标题和图标
st.set_page_config(
    page_title="NEON-CHAT 2119", 
    page_icon="💬",
    layout="wide"
)

# 获取随机头像
def get_random_avatar(seed):
    avatar_type = random.choice(AVATAR_URLS)
    return f"{avatar_type}{seed}"

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
    
    /* 密码输入框动画 */
    @keyframes flicker {
        0%, 19%, 21%, 23%, 25%, 54%, 56%, 100% {
            box-shadow: 0 0 10px var(--primary-color), 
                        0 0 20px var(--secondary-color);
        }
        20%, 24%, 55% {
            box-shadow: 0 0 7px var(--primary-color), 
                        0 0 10px var(--secondary-color);
        }
    }
    
    .password-input {
        animation: flicker 3s infinite;
    }
    
    /* 登录容器 */
    .login-container {
        position: relative;
        width: 100%;
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    .login-box {
        position: relative;
        width: 400px;
        padding: 40px;
        background: rgba(13, 2, 33, 0.8);
        box-shadow: 0 0 30px var(--primary-color);
        border: 1px solid var(--primary-color);
        border-radius: 5px;
        text-align: center;
    }
    
    /* 二进制背景动画 */
    .binary-bg {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        overflow: hidden;
        z-index: -1;
    }
    
    .binary-code {
        position: absolute;
        color: rgba(5, 217, 232, 0.1);
        font-size: 16px;
        user-select: none;
        animation: fall linear infinite;
    }
    
    @keyframes fall {
        to {
            transform: translateY(100vh);
        }
    }
    
    /* 头像样式 */
    .avatar-container {
        width: 80px;
        height: 80px;
        margin: 0 auto 20px;
        border: 2px solid var(--primary-color);
        border-radius: 50%;
        overflow: hidden;
        box-shadow: 0 0 15px var(--primary-color);
    }
    
    .avatar-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    
    /* 密码锁样式 */
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .cyberpunk-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, 
            #0d0221 0%, 
            #ff2a6d 25%, 
            #05d9e8 50%, 
            #d300c5 75%, 
            #0d0221 100%);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        z-index: -2;
    }
    
    .grid-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            linear-gradient(rgba(5, 217, 232, 0.1) 1px, transparent 1px),
            linear-gradient(90deg, rgba(5, 217, 232, 0.1) 1px, transparent 1px);
        background-size: 20px 20px;
        z-index: -1;
    }
    
    .cyberpunk-circle {
        position: fixed;
        border-radius: 50%;
        filter: blur(60px);
        opacity: 0.5;
        z-index: -1;
    }
    
    .circle-1 {
        width: 300px;
        height: 300px;
        background: #ff2a6d;
        top: 20%;
        left: 10%;
        animation: float 8s ease-in-out infinite;
    }
    
    .circle-2 {
        width: 400px;
        height: 400px;
        background: #05d9e8;
        bottom: 15%;
        right: 10%;
        animation: float 10s ease-in-out infinite;
    }
    
    .circle-3 {
        width: 200px;
        height: 200px;
        background: #d300c5;
        top: 60%;
        left: 30%;
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0) translateX(0); }
        50% { transform: translateY(-20px) translateX(20px); }
    }
    
    .password-lock {
        position: relative;
        width: 300px;
        height: 400px;
        margin: 0 auto;
        perspective: 1000px;
    }
    
    .lock-body {
        position: relative;
        width: 100%;
        height: 100%;
        transform-style: preserve-3d;
        transition: all 0.5s ease;
    }
    
    .lock-front, .lock-back {
        position: absolute;
        width: 100%;
        height: 100%;
        backface-visibility: hidden;
        background: rgba(13, 2, 33, 0.8);
        border: 2px solid #ff2a6d;
        border-radius: 10px;
        box-shadow: 0 0 20px #ff2a6d, 
                    0 0 40px #05d9e8,
                    inset 0 0 10px rgba(5, 217, 232, 0.3);
        padding: 30px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    
    .lock-back {
        transform: rotateY(180deg);
        background: rgba(255, 42, 109, 0.8);
    }
    
    .lock-title {
        color: #05d9e8;
        text-shadow: 0 0 10px #05d9e8;
        font-size: 24px;
        margin-bottom: 30px;
        text-align: center;
    }
    
    .lock-input {
        background: transparent;
        border: 1px solid #05d9e8;
        color: #ff2a6d;
        padding: 15px;
        width: 100%;
        margin-bottom: 20px;
        font-size: 18px;
        text-align: center;
        outline: none;
        box-shadow: 0 0 10px rgba(5, 217, 232, 0.3);
        transition: all 0.3s;
    }
    
    .lock-input:focus {
        border-color: #ff2a6d;
        box-shadow: 0 0 15px #ff2a6d;
    }
    
    .lock-button {
        background: linear-gradient(45deg, #ff2a6d, #d300c5);
        color: white;
        border: none;
        padding: 12px 30px;
        font-size: 16px;
        cursor: pointer;
        border-radius: 5px;
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: all 0.3s;
        box-shadow: 0 0 10px rgba(255, 42, 109, 0.5);
        margin-top: 20px;
    }
    
    .lock-button:hover {
        background: linear-gradient(45deg, #d300c5, #ff2a6d);
        box-shadow: 0 0 20px #ff2a6d;
    }
    
    .lock-indicator {
        width: 100%;
        height: 10px;
        background: rgba(5, 217, 232, 0.2);
        border-radius: 5px;
        margin-bottom: 20px;
        overflow: hidden;
        position: relative;
    }
    
    .lock-progress {
        height: 100%;
        width: 0%;
        background: linear-gradient(90deg, #05d9e8, #ff2a6d);
        transition: width 0.3s;
    }
    
    .lock-hologram {
        position: absolute;
        width: 80%;
        height: 150px;
        background: linear-gradient(135deg, rgba(5, 217, 232, 0.1), rgba(255, 42, 109, 0.1));
        border: 1px solid #05d9e8;
        border-radius: 10px;
        top: -170px;
        left: 10%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 20px rgba(5, 217, 232, 0.3);
    }
    
    .hologram-text {
        color: #05d9e8;
        font-size: 14px;
        text-align: center;
        text-shadow: 0 0 5px #05d9e8;
        animation: hologram-flicker 2s infinite alternate;
    }
    
    @keyframes hologram-flicker {
        0%, 100% { opacity: 0.8; }
        50% { opacity: 0.3; }
    }
    
    .lock-digits {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin-bottom: 30px;
    }
    
    .digit {
        width: 30px;
        height: 40px;
        background: rgba(5, 217, 232, 0.1);
        border: 1px solid #05d9e8;
        color: #ff2a6d;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        position: relative;
    }
    
    .digit::after {
        content: "";
        position: absolute;
        bottom: 5px;
        width: 10px;
        height: 2px;
        background: #05d9e8;
    }
    
    .lock-keypad {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 15px;
        width: 100%;
    }
    
    .key {
        background: rgba(13, 2, 33, 0.5);
        border: 1px solid #05d9e8;
        color: #05d9e8;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        cursor: pointer;
        transition: all 0.2s;
        border-radius: 5px;
    }
    
    .key:hover {
        background: rgba(255, 42, 109, 0.3);
        box-shadow: 0 0 10px #ff2a6d;
    }
    
    .key:active {
        transform: scale(0.95);
    }
    
    .key-clear {
        grid-column: span 3;
        background: rgba(255, 42, 109, 0.3);
    }
    
    .access-granted {
        color: #05d9e8;
        font-size: 24px;
        text-align: center;
        margin-top: 20px;
        text-shadow: 0 0 10px #05d9e8;
        animation: pulse 1.5s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .access-denied {
        color: #ff2a6d;
        font-size: 24px;
        text-align: center;
        margin-top: 20px;
        text-shadow: 0 0 10px #ff2a6d;
        animation: shake 0.5s;
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        20%, 60% { transform: translateX(-5px); }
        40%, 80% { transform: translateX(5px); }
    }
    </style>
    """, unsafe_allow_html=True)

# 初始化聊天记录文件（如果不存在）
if not os.path.exists(CHAT_FILE):
    pd.DataFrame(columns=['timestamp', 'user', 'message', 'avatar']).to_csv(CHAT_FILE, index=False)

# 加载聊天记录
def load_messages():
    return pd.read_csv(CHAT_FILE)

# 保存新消息到聊天记录
def save_message(user, message):
    if not user or not message:  # 确保用户名和消息都不为空
        return
    
    # 获取或生成用户头像
    if 'avatar_url' not in st.session_state or not st.session_state.avatar_url:
        st.session_state.avatar_url = get_random_avatar(user)
    
    new_message = pd.DataFrame([{
        'timestamp': datetime.now().strftime("%H:%M:%S"),
        'user': user.strip(),  # 去除前后空格
        'message': message,
        'avatar': st.session_state.avatar_url
    }])
    new_message.to_csv(CHAT_FILE, mode='a', index=False, header=False)

# 清空聊天记录
def clear_messages():
    pd.DataFrame(columns=['timestamp', 'user', 'message', 'avatar']).to_csv(CHAT_FILE, index=False)

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

# 检查密码
def check_password():
    """返回是否通过密码验证"""
    if 'password_correct' not in st.session_state:
        st.session_state.password_correct = False
    
    if st.session_state.password_correct:
        return True
    
    # 创建炫酷的赛博朋克背景
    st.markdown("""
    <div class="cyberpunk-bg"></div>
    <div class="grid-overlay"></div>
    <div class="cyberpunk-circle circle-1"></div>
    <div class="cyberpunk-circle circle-2"></div>
    <div class="cyberpunk-circle circle-3"></div>
    """, unsafe_allow_html=True)
    
    # 密码锁界面
    st.markdown("""
    <div style="display: flex; justify-content: center; align-items: center; height: 100vh;">
        <div class="password-lock">
            <div class="lock-body" id="lockBody">
                <div class="lock-front">
                    <div class="lock-hologram">
                        <div class="hologram-text">
                            NEURAL INTERFACE TERMINAL<br>
                            VERIFICATION REQUIRED<br>
                            UNAUTHORIZED ACCESS WILL BE<br>
                            REPORTED TO CYBERSECURITY
                        </div>
                    </div>
                    
                    <h2 class="lock-title">NEON-CHAT 2119</h2>
                    
                    <div class="lock-indicator">
                        <div class="lock-progress" id="lockProgress"></div>
                    </div>
                    
                    <div class="lock-digits" id="lockDigits">
                        <div class="digit"></div>
                        <div class="digit"></div>
                        <div class="digit"></div>
                        <div class="digit"></div>
                        <div class="digit"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 使用Streamlit表单处理密码输入
    with st.form("password_form", clear_on_submit=True):
        password = st.text_input("Enter Password", type="password", label_visibility="collapsed")
        submitted = st.form_submit_button("AUTHENTICATE")
        
        if submitted:
            if password == CORRECT_PASSWORD:
                st.session_state.password_correct = True
                st.success("ACCESS GRANTED. INITIALIZING NEURAL INTERFACE...")
                time.sleep(1)
                st.rerun()
            else:
                st.error("ACCESS DENIED. INCORRECT PASSCODE.")
    
    return False

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
            st.session_state.avatar_url = ""

        new_name = st.text_input("USER IDENTITY", value=st.session_state.user_name)
        if new_name != st.session_state.user_name:
            if new_name.strip():
                st.session_state.user_name = new_name.strip()
                st.session_state.avatar_url = get_random_avatar(new_name.strip())
                st.success(f"IDENTITY CONFIRMED: {new_name}")
                
                # 显示用户头像
                st.markdown(f"""
                <div style="text-align: center; margin: 20px 0;">
                    <div class="avatar-container">
                        <img src="{st.session_state.avatar_url}" class="avatar-img" alt="User Avatar">
                    </div>
                    <div style="color: #05d9e8; margin-top: 10px;">USER: {new_name.strip()}</div>
                </div>
                """, unsafe_allow_html=True)
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
            # 为每个用户创建自定义聊天消息
            avatar_html = f"<img src='{row['avatar']}' width='40' style='border-radius: 50%; border: 2px solid #ff2a6d;'>" if pd.notna(row['avatar']) else ""
            
            with st.chat_message(name=str(row['user']).strip()):
                st.markdown(f"""
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 5px;">
                    {avatar_html}
                    <div>
                        <span style="color: #ff2a6d; font-weight: bold;">{row['user']}</span> 
                        <span style="color: #05d9e8; font-size: 0.8em;">[{row['timestamp']}]</span>
                    </div>
                </div>
                <div style="color: #d1f7ff; margin-left: 50px;">
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
            avatar_html = f"<img src='{st.session_state.avatar_url}' width='40' style='border-radius: 50%; border: 2px solid #ff2a6d;'>" if hasattr(st.session_state, 'avatar_url') and st.session_state.avatar_url else ""
            
            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 5px;">
                {avatar_html}
                <div>
                    <span style="color: #ff2a6d; font-weight: bold;">{st.session_state.user_name}</span> 
                    <span style="color: #05d9e8; font-size: 0.8em;">[{datetime.now().strftime('%H:%M:%S')}]</span>
                </div>
            </div>
            <div style="color: #d1f7ff; margin-left: 50px;">
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
