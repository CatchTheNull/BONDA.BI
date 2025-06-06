import streamlit as st

# --- Статичный код ---
STATIC_VERIFICATION_CODE = "123456"

# --- Авторизация по email (упрощённая, без отправки) ---
def email_auth():
    st.subheader("🔐 Авторизация")

    if not st.session_state.get("authenticated"):
        email = st.text_input("Введите email", value="bondabi@yandex.ru")
        code_input = st.text_input("Введите код", help="Для проверки введите: 123456")

        if st.button("🔓 Войти") and code_input:
            if code_input == STATIC_VERIFICATION_CODE:
                st.success("✅ Авторизация успешна")
                st.session_state.authenticated = True
                st.session_state.entered_email = email
                st.rerun()
            else:
                st.error("❌ Неверный код")
        st.stop()
