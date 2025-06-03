# auth_handler.py
import os
import random
import smtplib
from dotenv import load_dotenv
import streamlit as st
from email.mime.text import MIMEText

# --- Загрузка .env ---
load_dotenv()
SMTP_SERVER = "smtp.yandex.ru"
SMTP_PORT = 587
SMTP_USER = os.getenv("SMTP_USERNAME")
SMTP_PASS = os.getenv("SMTP_PASSWORD")

# --- Генерация кода ---
def generate_code():
    return str(random.randint(100000, 999999))

# --- Отправка кода ---
def send_code(email: str, code: str):
    message = MIMEText(f"Ваш код подтверждения: {code}")
    message['Subject'] = "Код подтверждения BONDA.BIZ"
    message['From'] = SMTP_USER
    message['To'] = email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, email, message.as_string())
        st.success(f"Код отправлен на {email}")
    except Exception as e:
        st.error("❌ Ошибка отправки письма")
        st.exception(e)

# --- Авторизация ---
def email_auth():
    st.subheader("🔐 Авторизация по email")

    if 'email_sent' not in st.session_state:
        st.session_state.email_sent = False

    email = st.text_input("Введите email")

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