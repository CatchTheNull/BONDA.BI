# auth_handler.py
import os
import random
from dotenv import load_dotenv
import yagmail
import streamlit as st

# --- Загрузка .env ---
load_dotenv()
SMTP_USER = os.getenv("SMTP_USERNAME")
SMTP_PASS = os.getenv("SMTP_PASSWORD")

# --- Инициализация SMTP клиента ---
yag = yagmail.SMTP(SMTP_USER, SMTP_PASS, oauth2_file=False)

# --- Генерация 6-значного кода ---
def generate_code():
    return str(random.randint(100000, 999999))

# --- Отправка кода на email ---
def send_code(email: str, code: str):
    subject = "Код подтверждения BONDA.BIZ"
    body = f"Ваш код подтверждения: {code}"
    try:
        yag.send(to=email, subject=subject, contents=body)
        st.success(f"Код отправлен на {email}")
    except Exception as e:
        st.error("Ошибка отправки email")
        st.exception(e)

# --- Основной метод авторизации ---
def email_auth():
    st.subheader("🔐 Авторизация")

    if "code_sent" not in st.session_state:
        st.session_state.code_sent = False

    if not st.session_state.code_sent:
        email = st.text_input("Введите ваш email")
        if st.button("📤 Отправить код") and email:
            code = generate_code()
            st.session_state.verification_code = code
            st.session_state.entered_email = email
            send_code(email, code)
            st.session_state.code_sent = True
            st.experimental_rerun()

    else:
        code_input = st.text_input("Введите код из письма")
        if st.button("✅ Подтвердить"):
            if code_input == st.session_state.get("verification_code"):
                st.success("✅ Авторизация успешна")
                st.session_state.authenticated = True
                # Сбросить состояние после успешной авторизации
                st.session_state.code_sent = False
            else:
                st.error("❌ Неверный код. Попробуйте ещё раз.")
                if st.button("🔁 Отправить заново"):
                    st.session_state.code_sent = False
                    st.experimental_rerun()