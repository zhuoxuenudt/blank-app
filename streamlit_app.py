import streamlit as st
from datetime import datetime
import pandas as pd
import os
import time
from twilio.rest import Client
import requests
import random
import string

# 共享聊天记录文件名
CHAT_FILE = "chat_history.csv"

# 安全配置
CORRECT_PASSWORD = "hello world"  # 主密码
VERIFICATION_CODE = "2119"       # 操作验证码
SERVER_CHAN_TITLE = "【SYSTEM ALERT】NEON-CHAT 2119 NOTIFICATION"  # 固定通知标题

# Twilio配置
ACCOUNT_SID = "AC6d70171e378d8da26ee5521c78214382"
AUTH_TOKEN = "39af64209304f3a8b82b83b10ca899c4"
TWILIO_PHONE = "+13412182075"
TO_PHONE = "+8615616139621"

# Server酱配置
SERVER_CHAN_URL = "https://sctapi.ftqq.com/SCT31129TtqguxCLA1OYNhAf1mtxxmyz3.send"

# 卡通头像URL
AVATAR_URL = "https://api.dicebear.com/7.x/bottts/svg?seed="

# 设置页面
st.set_page_config(
    page_title="NEON-CHAT 2119", 
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="collapsed"
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
        font-family: 'Orbitron', 'Courier New', monospace;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0d0221 0%, #1a1b3a 100%);
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: var(--primary-color);
        text-shadow: 0 0 5px var(--primary-color), 0 0 20px var(--primary-color);
        font-weight: 900;
        letter-spacing: 2px;
    }
    
    /* 登录页面特定样式 */
    .login-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        background: url('https://images.unsplash.com/photo-1534796636912-3b95b3ab5986?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80') no-repeat center center;
        background-size: cover;
        z-index: -1;
    }
    
    .login-overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(13, 2, 33, 0.85);
    }
    
    .login-box {
        position: relative;
        width: 600px;
        padding: 50px;
        background: rgba(13, 2, 33, 0.9);
        border: 2px solid var(--primary-color);
        box-shadow: 0 0 30px var(--primary-color), 0 0 60px var(--secondary-color);
        text-align: center;
        z-index: 1;
        animation: pulse 2s infinite alternate;
    }
    
    @keyframes pulse {
        from {
            box-shadow: 0 0 30px var(--primary-color), 0 0 60px var(--secondary-color);
        }
        to {
            box-shadow: 0 0 40px var(--primary-color), 0 0 80px var(--secondary-color);
        }
    }
    
    .login-title {
        font-size: 4rem;
        margin-bottom: 10px;
        background: linear-gradient(90deg, #ff2a6d, #05d9e8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-transform: uppercase;
    }
    
    .login-subtitle {
        font-size: 1.5rem;
        color: var(--secondary-color);
        margin-bottom: 40px;
        letter-spacing: 5px;
    }
    
    .password-input {
        font-size: 1.5rem;
        letter-spacing: 5px;
        text-align: center;
        margin: 30px 0;
    }
    
    /* 主界面样式 */
    .main-container {
        padding: 20px;
    }
    
    /* 其他样式保持不变... */
    </style>
    """, unsafe_allow_html=True)

    # 添加Orbitron字体
    st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

# 检查密码
def check_password():
    """返回是否通过密码验证"""
    if 'password_correct' not in st.session_state:
        st.session_state.password_correct = False
    
    if st.session_state.password_correct:
        return True
    
    # 创建二进制背景动画
    create_binary_background()
    
    # 赛博朋克风格的登录界面 - 增强版
    st.markdown("""
    <div class="login-container">
        <div class="login-box">
            <h1 style="color: #ff2a6d; text-shadow: 0 0 20px #ff2a6d, 0 0 40px #ff2a6d; font-size: 5rem; margin-bottom: 0.5rem;">2119</h1>
            <p style="color: #05d9e8; font-size: 2rem; margin-bottom: 2rem; text-shadow: 0 0 10px #05d9e8;">NEURAL INTERFACE TERMINAL</p>
            
            <!-- 动态扫描线效果 -->
            <div style="position: relative; height: 2px; width: 100%; margin: 2rem 0; overflow: hidden;">
                <div style="position: absolute; height: 100%; width: 100%; background: linear-gradient(90deg, transparent, #ff2a6d, transparent); animation: scan 2s linear infinite;"></div>
            </div>
            
            <!-- 创意密码输入框 -->
            <div style="position: relative; margin: 3rem 0;">
                <div class="terminal password-input" style="height: 80px; display: flex; align-items: center; justify-content: center;">
                    <div id="password-dots" style="letter-spacing: 1rem; font-size: 2rem; color: #05d9e8;"></div>
                    <input type="password" id="hidden-password-input" style="opacity: 0; position: absolute; width: 0; height: 0;">
                </div>
                <div style="color: #05d9e8; margin-top: 1rem; font-size: 1.2rem; text-align: center;">
                    <span id="password-status">ENTER ACCESS CODE</span>
                </div>
            </div>
            
            <!-- 认证按钮 -->
            <div style="position: relative;">
                <button id="auth-button" style="background: transparent; border: 2px solid #05d9e8; color: #05d9e8; padding: 1rem 3rem; font-size: 1.5rem; cursor: pointer; text-transform: uppercase; letter-spacing: 0.5rem; position: relative; overflow: hidden; transition: all 0.3s;">
                    <span style="position: relative; z-index: 2;">AUTHENTICATE</span>
                    <span style="position: absolute; top: 0; left: -100%; width: 100%; height: 100%; background: linear-gradient(90deg, transparent, rgba(5, 217, 232, 0.5), transparent); transition: all 0.6s;"></span>
                </button>
            </div>
        </div>
    </div>
    
    <style>
    @keyframes scan {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    @keyframes pulse {
        0%, 100% { box-shadow: 0 0 10px #ff2a6d, 0 0 20px #05d9e8; }
        50% { box-shadow: 0 0 20px #ff2a6d, 0 0 40px #05d9e8; }
    }
    
    .password-input {
        animation: pulse 2s infinite;
        position: relative;
    }
    
    #auth-button:hover {
        background: rgba(5, 217, 232, 0.1) !important;
        box-shadow: 0 0 15px #05d9e8;
    }
    
    #auth-button:hover span:last-child {
        left: 100%;
    }
    
    /* 密码点动画 */
    @keyframes dot-appear {
        0% { opacity: 0; transform: scale(0.5); }
        100% { opacity: 1; transform: scale(1); }
    }
    
    .password-dot {
        display: inline-block;
        animation: dot-appear 0.3s ease-out;
    }
    </style>
    
    <script>
    // 密码输入处理
    const passwordDots = document.getElementById('password-dots');
    const hiddenInput = document.getElementById('hidden-password-input');
    const passwordStatus = document.getElementById('password-status');
    let password = '';
    
    // 聚焦到隐藏的输入框
    hiddenInput.focus();
    
    // 监听输入
    hiddenInput.addEventListener('input', (e) => {
        password = e.target.value;
        
        // 更新显示的圆点
        passwordDots.innerHTML = '';
        for (let i = 0; i < password.length; i++) {
            const dot = document.createElement('span');
            dot.className = 'password-dot';
            dot.innerHTML = '•';
            passwordDots.appendChild(dot);
        }
        
        // 更新状态文本
        if (password.length > 0) {
            passwordStatus.textContent = 'ACCESS CODE: ' + '*'.repeat(password.length);
        } else {
            passwordStatus.textContent = 'ENTER ACCESS CODE';
        }
    });
    
    // 按钮点击处理
    document.getElementById('auth-button').addEventListener('click', () => {
        // 这里将通过Streamlit的通信机制发送密码
        window.parent.postMessage({
            type: 'streamlit:setComponentValue',
            value: password
        }, '*');
    });
    </script>
    """, unsafe_allow_html=True)
    
    # 使用Streamlit的通信机制获取密码
    password = st.text_input(" ", type="password", key="password_input", 
                           label_visibility="collapsed")
    
    if st.button(" ", key="auth_submit", use_container_width=True):
        if password == CORRECT_PASSWORD:
            st.session_state.password_correct = True
            st.success("ACCESS GRANTED. INITIALIZING NEURAL INTERFACE...")
            time.sleep(1)
            st.rerun()
        else:
            st.error("UNAUTHORIZED ACCESS DETECTED. SYSTEM LOCKDOWN INITIATED.")
            # 添加震动效果
            st.markdown("""
            <script>
            document.querySelector('.login-box').animate([
                { transform: 'translateX(0)' },
                { transform: 'translateX(-10px)' },
                { transform: 'translateX(10px)' },
                { transform: 'translateX(-10px)' },
                { transform: 'translateX(10px)' },
                { transform: 'translateX(-10px)' },
                { transform: 'translateX(0)' }
            ], {
                duration: 500,
                iterations: 1
            });
            </script>
            """, unsafe_allow_html=True)
    
    return False

# 初始化聊天记录文件
if not os.path.exists(CHAT_FILE):
    pd.DataFrame(columns=['timestamp', 'user', 'message', 'avatar']).to_csv(CHAT_FILE, index=False)

# 加载聊天记录
def load_messages():
    return pd.read_csv(CHAT_FILE)

# 保存新消息
def save_message(user, message):
    if not user or not message:
        return
    
    if 'avatar_url' not in st.session_state:
        st.session_state.avatar_url = f"{AVATAR_URL}{user}"
    
    new_message = pd.DataFrame([{
        'timestamp': datetime.now().strftime("%H:%M:%S"),
        'user': user.strip(),
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
def send_serverchan_message(message):
    data = {
        "title": SERVER_CHAN_TITLE,
        "desp": message,
        "channel": 9
    }
    
    try:
        response = requests.post(SERVER_CHAN_URL, data=data)
        response.raise_for_status()
        return True, response.json()
    except requests.exceptions.RequestException as e:
        return False, str(e)

# 验证操作权限
def verify_operation():
    """验证敏感操作"""
    with st.expander("🔐 SECURITY VERIFICATION", expanded=True):
        code = st.text_input("ENTER VERIFICATION CODE", type="password")
        if st.button("VERIFY"):
            if code == VERIFICATION_CODE:
                st.session_state.verified = True
                st.success("VERIFICATION SUCCESSFUL")
                return True
            else:
                st.error("INVALID VERIFICATION CODE")
                st.session_state.verified = False
                return False
    return False

# 主应用
def main_app():
    set_cyberpunk_style()
    
    # 侧边栏 - 用户设置
    with st.sidebar:
        st.markdown("""
        <div style="border-bottom: 2px solid #ff2a6d; padding-bottom: 10px; margin-bottom: 20px;">
            <h2 style="color: #05d9e8;">SYSTEM CONTROL PANEL</h2>
        </div>
        """, unsafe_allow_html=True)

        # 用户名和头像
        if 'user_name' not in st.session_state:
            st.session_state.user_name = ""
        
        new_name = st.text_input("USER IDENTITY", value=st.session_state.user_name)
        if new_name != st.session_state.user_name:
            if new_name.strip():
                st.session_state.user_name = new_name.strip()
                st.session_state.avatar_url = f"{AVATAR_URL}{new_name.strip()}"
                st.success(f"IDENTITY CONFIRMED: {new_name}")
                
                st.markdown(f"""
                <div style="text-align: center; margin: 20px 0;">
                    <img src="{st.session_state.avatar_url}" width="80" style="border-radius: 50%; border: 2px solid #ff2a6d; box-shadow: 0 0 15px #ff2a6d;">
                    <div style="color: #05d9e8; margin-top: 10px;">USER: {new_name.strip()}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("IDENTITY REQUIRED FOR NEURAL UPLINK")

        # 清空聊天记录按钮 (需要验证)
        st.markdown("""
        <div style="border-top: 2px solid #ff2a6d; margin: 20px 0; padding-top: 10px;">
            <h3 style="color: #05d9e8;">ADMINISTRATIVE FUNCTIONS</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("PURGE MEMORY BANKS", key="clear_chat"):
            if verify_operation():
                clear_messages()
                st.success("MEMORY PURGE COMPLETE")
        
        # 消息通知功能 (需要验证)
        with st.form("serverchan_form"):
            st.markdown("<h4 style='color: #ff2a6d;'>SYSTEM ALERT TRANSMITTER</h4>", unsafe_allow_html=True)
            message = st.text_area("ALERT MESSAGE")
            submitted = st.form_submit_button("SEND ALERT")
            
            if submitted:
                if not message:
                    st.warning("MESSAGE CONTENT REQUIRED")
                elif verify_operation():
                    success, result = send_serverchan_message(message)
                    if success:
                        st.success("ALERT TRANSMITTED SUCCESSFULLY")
                        st.json(result)
                    else:
                        st.error(f"TRANSMISSION FAILED: {result}")

    # 主界面
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
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 5px;">
                    <img src="{row['avatar']}" width="40" style="border-radius: 50%; border: 2px solid #ff2a6d;">
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

        save_message(st.session_state.user_name, prompt)
        st.rerun()

    # 自动刷新
    time.sleep(5)
    st.rerun()

# 应用入口
if not check_password():
    st.stop()

main_app()
