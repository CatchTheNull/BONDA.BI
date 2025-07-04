import streamlit as st

# --- Фиксированный тестовый код ---
TEST_VERIFICATION_CODE = "123456"

# --- Отправка письма (имитация) ---
def send_code(email: str, code: str):
    st.info(f"Письмо отправлено на {email}. Используй код: {code}")

# --- Авторизация по email ---
def email_auth():
    st.subheader("🔐 Авторизация по email")

    if 'email_sent' not in st.session_state:
        st.session_state.email_sent = False

    email = st.text_input("Введите email")

    if not st.session_state.email_sent and st.button("📤 Отправить код") and email:
        st.session_state.verification_code = TEST_VERIFICATION_CODE
        st.session_state.entered_email = email
        st.session_state.email_sent = True
        send_code(email, TEST_VERIFICATION_CODE)

    if st.session_state.email_sent:
        code_input = st.text_input("Введите код из письма")
        if code_input:
            if code_input == TEST_VERIFICATION_CODE:
                st.success("✅ Авторизация успешна")
                st.session_state.authenticated = True
            else:
                st.error("❌ Неверный код")