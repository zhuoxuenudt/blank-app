# Home.py
import streamlit as st

# 配置密码
CORRECT_PASSWORD = "123456"

st.set_page_config(page_title="登录聊天室", page_icon="🔐")

def check_password():
    if 'password_correct' not in st.session_state:
        st.session_state.password_correct = False

    if st.session_state.password_correct:
        st.switch_page("pages/Chatroom.py")

    with st.form("密码验证"):
        password = st.text_input("请输入密码", type="password")
        submitted = st.form_submit_button("提交")

        if submitted:
            if password == CORRECT_PASSWORD:
                st.session_state.password_correct = True
                st.success("密码正确！正在进入聊天室...")
                st.switch_page("pages/Chatroom.py")
            else:
                st.error("密码错误，请重试")

# 页面主入口
st.title("🔐 登录聊天室")
check_password()
