import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard по продажам", layout="wide")
st.title("📊 Dashboard по продажам")

uploaded_file = st.file_uploader("Загрузите Excel-файл отчета из iiko", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file, skiprows=4)
    df = df[pd.to_datetime(df['Учетный день'], errors='coerce').notna()]
    df = df[df['Тип оплаты'].notna()]
    df.columns = ['date', 'restaurant', 'group', 'payment_type', 'amount', 'checks']
    df['date'] = pd.to_datetime(df['date']).dt.date
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    df['checks'] = pd.to_numeric(df['checks'], errors='coerce')

    selected_date = st.selectbox("📅 Выберите дату", sorted(df['date'].unique()))
    filtered = df[df['date'] == selected_date]

    st.subheader("💰 Выручка по типам оплат")
    revenue = filtered.groupby('payment_type')['amount'].sum().reset_index()
    st.plotly_chart(px.bar(revenue, x="payment_type", y="amount", title="Выручка"), use_container_width=True)

    st.subheader("🧾 Количество чеков по типам оплат")
    checks = filtered.groupby('payment_type')['checks'].sum().reset_index()
    st.plotly_chart(px.bar(checks, x="payment_type", y="checks", title="Чеки"), use_container_width=True)