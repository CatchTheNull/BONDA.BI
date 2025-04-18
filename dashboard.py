import streamlit as st
import pandas as pd
import plotly.express as px
import time
import random

# ВАЖНО: ставим первым!
st.set_page_config(page_title="BONDA BI – Отчёт по продажам", layout="wide")

# --- ЛОАДЕР: логотип + фразы ---
def show_loader():
    phrases = [
        "👨‍🍳 Генерируем повара-гения…",
        "📈 Строим графики из соуса демиглас…",
        "💡 Симулируем инсайты как в топовой франшизе...",
        "🥂 Рассчитываем ROI для бокала Просекко…",
        "🧠 Наблюдаем за очень умным BI-аналитиком...",
        "🍽️ Подгружаем лучшие практики из Michelin…",
        "💰 Моделируем выручку с учётом отмен и чаевых...",
        "🔍 Складываем чеки как Lego…",
        "📊 Симулируем эмоции кассира в момент скидки…",
    ]

    phrase = random.choice(phrases)

    st.markdown(f"""
        <style>
        .loader-wrapper {{
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            position: relative;
        }}
        .fade-text {{
            position: absolute;
            top: 15%;
            font-size: 1.3em;
            color: white;
            text-align: center;
            animation: fadeIn 1s ease-in-out forwards;
        }}
        .logo {{
            max-width: 300px;
            animation: fadeIn 1.2s ease-in-out forwards;
        }}
        .progress-bar {{
            position: absolute;
            top: 23%;
            width: 200px;
            height: 8px;
            background-color: #333;
            border-radius: 4px;
            overflow: hidden;
        }}
        .bar-fill {{
            height: 100%;
            background-color: #FF8C00;
            width: 0%;
            transition: width 1s;
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}
        </style>

        <div class="loader-wrapper">
            <div class="fade-text">{phrase}</div>
            <div class="progress-bar"><div class="bar-fill" id="bar"></div></div>
            <img src="https://raw.githubusercontent.com/CatchTheNull/BONDA.BI/main/bonda-logo.png" class="logo">
        </div>

        <script>
        let i = 0;
        const fill = document.getElementById('bar');
        const interval = setInterval(() => {{
            i++;
            fill.style.width = (i * 20) + '%';
            if (i >= 5) clearInterval(interval);
        }}, 1000);
        </script>
    """, unsafe_allow_html=True)

    time.sleep(5)
# --- ЗАГОЛОВОК ---
st.title("📊 BI-Дэшборд по продажам")

# --- ЗАГРУЗКА ФАЙЛА ---
uploaded_file = st.file_uploader("Загрузите Excel OLAP отчёт", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file, skiprows=4)
    df = df[pd.to_datetime(df['Учетный день'], errors='coerce').notna()]
    df = df[df['Тип оплаты'].notna()]
    df.columns = ['date', 'restaurant', 'group', 'payment_type', 'amount', 'checks']
    df['date'] = pd.to_datetime(df['date']).dt.date
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    df['checks'] = pd.to_numeric(df['checks'], errors='coerce')

    # ФИЛЬТРЫ
    col1, col2 = st.columns(2)
    with col1:
        date_options = ["Все даты"] + sorted(df['date'].unique())
        selected_date = st.selectbox("📅 Выберите дату", date_options)
    with col2:
        all_restaurants = ["Все точки"] + sorted(df['restaurant'].unique())
        selected_restaurant = st.selectbox("🏪 Выберите точку продаж", all_restaurants)

    # ФИЛЬТРАЦИЯ
    if selected_date == "Все даты":
        filtered = df.copy()
    else:
        filtered = df[df['date'] == selected_date]

    if selected_restaurant != "Все точки":
        filtered = filtered[filtered['restaurant'] == selected_restaurant]

    # ДАННЫЕ ДЛЯ ГРАФИКОВ
    total_sum = int(filtered['amount'].sum())
    pie_data = filtered.groupby('payment_type')['amount'].sum().reset_index()
    checks_data = filtered.groupby('restaurant')['checks'].sum().reset_index()
    revenue_data = filtered.groupby('restaurant')['amount'].sum().reset_index()

    # ВИЗУАЛИЗАЦИЯ
    st.markdown("### 📈 Визуализация показателей")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("💳 Типы оплат")
        fig = px.pie(pie_data, names='payment_type', values='amount', hole=0.5)
        fig.update_traces(textinfo='label+percent', hoverinfo="label+value")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(f"#### 💰 {total_sum:,.0f} ₽")

    with col2:
        st.subheader("🧾 Количество чеков")
        fig2 = px.bar(checks_data, x='restaurant', y='checks', text='checks', color='restaurant')
        fig2.update_layout(showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    with col3:
        st.subheader("🏷️ Сумма продаж по точкам")
        fig3 = px.bar(revenue_data, x='restaurant', y='amount', text='amount', color='restaurant')
        fig3.update_layout(showlegend=False)
        st.plotly_chart(fig3, use_container_width=True)

    # ТАБЛИЦА
    st.markdown("### 📄 Детализация по точкам")
    detail = filtered.groupby('restaurant').agg({
        'amount': 'sum',
        'checks': 'sum'
    }).reset_index()

    def flag(row):
        flags = []
        if row['checks'] < 10:
            flags.append("Мало чеков")
        if row['amount'] < 100:
            flags.append("Низкая выручка")
        return ", ".join(flags) if flags else "-"

    detail['Флаги'] = detail.apply(flag, axis=1)
    detail['amount'] = detail['amount'].apply(lambda x: f"{int(x):,} ₽".replace(",", " "))

    st.dataframe(detail.rename(columns={
        'restaurant': 'Точка',
        'amount': 'Выручка',
        'checks': 'Чеки'
    }), use_container_width=True)

    # ВЫГРУЗКА
    st.download_button("📥 Выгрузить таблицу в Excel", data=detail.to_csv(index=False).encode('utf-8'), file_name="report.csv", mime="text/csv")