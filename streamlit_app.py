import streamlit as st
import time

# 设置密码
CORRECT_PASSWORD = "123456"

# 页面配置
st.set_page_config(page_title="登录", page_icon="🔒")

def show_login_page():
    """显示登录页面"""
    st.title("🔒 聊天室登录")
    
    if 'password_correct' not in st.session_state:
        st.session_state.password_correct = False
    
    if st.session_state.password_correct:
        return True
    
    with st.form("login_form"):
        password = st.text_input("请输入密码", type="password")
        submitted = st.form_submit_button("登录")
        
        if submitted:
            if password == CORRECT_PASSWORD:
                st.session_state.password_correct = True
                st.success("密码正确！正在进入聊天室...")
                time.sleep(1)  # 让用户看到成功消息
                return True
            else:
                st.error("密码错误，请重试")
    
    return False

# 主逻辑
if show_login_page():
    # 登录成功后跳转到聊天室
    st.switch_page("chatroom.py")
