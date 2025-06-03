# auth_handler.py

import os
import random
import requests
import streamlit as st
from dotenv import load_dotenv

# --- Загрузка .env ---
load_dotenv()
RESEND_API_KEY = os.getenv("re_Cav7CHtK_CGv6WwaPmJVqU7wfwF9Kc9R4")

# --- Генерация 6-значного кода ---
def generate_code():
    return str(random.randint(100000, 999999))

# --- Отправка письма через Resend ---
def send_code(email: str, code: str):
    if email != "mkmatveev@gmail.com":
        st.warning("❗️На бесплатном тарифе Resend разрешена отправка только на email, указанный при регистрации (mkmatveev@gmail.com)")
        return

    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "from": "you@resend.dev",
        "to": [email],
        "subject": "Код подтверждения BONDA.BIZ",
        "html": f"<p>Ваш код подтверждения: <b>{code}</b></p>"
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            st.success(f"📤 Код отправлен на {email}")
        else:
            st.error("❌ Ошибка отправки письма")
            st.json(response.json())
    except Exception as e:
        st.error("❌ Ошибка при соединении с Resend")
        st.exception(e)

# --- Авторизация по email ---
def email_auth():
    st.subheader("🔐 Авторизация по email")

    if 'email_sent' not in st.session_state:
        st.session_state.email_sent = False

    email = st.text_input("Введите email", value="mkmatveev@gmail.com")

    if not st.session_state.email_sent and st.button("📤 Отправить код") and email:
        code = generate_code()
        send_code(email, code)
        st.session_state.verification_code = code
        st.session_state.entered_email = email
        st.session_state.email_sent = True

    if st.session_state.email_sent:
        code_input = st.text_input("Введите код из письма")
        if code_input:
            if code_input == st.session_state.verification_code:
                st.success("✅ Авторизация успешна")
                st.session_state.authenticated = True
            else:
                st.error("❌ Неверный код")