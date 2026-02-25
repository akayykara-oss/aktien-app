import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="NVIDIA Earnings Tracker", layout="wide")
API_KEY = "7WVP0MXARBW5EN7D"
SYMBOL = st.sidebar.text_input("Ticker Symbol", "NVDA").upper()

def get_json(func, sym):
    url = f"https://www.alphavantage.co/query?function={func}&symbol={sym}&apikey={API_KEY}"
    return requests.get(url).json()

st.title(f"🚀 Deep Dive: {SYMBOL}")

if SYMBOL:
    tab1, tab2, tab3 = st.tabs(["📈 Analyse", "📅 Earnings", "📰 News"])

    with tab2:
        st.subheader("Quartalszahlen & Analysten-Erwartungen")
        earnings_data = get_json("EARNINGS", SYMBOL)
        
        if "quarterlyEarnings" in earnings_data:
            # Die letzten 4 Quartale in einer Tabelle
            df = pd.DataFrame(earnings_data['quarterlyEarnings']).head(4)
            # Spalten umbenennen für besseres Verständnis
            df = df[['fiscalDateEnding', 'reportedEPS', 'estimatedEPS', 'surprisePercentage']]
            df.columns = ['Quartalsende', 'Gemeldeter Gewinn', 'Erwartet', 'Überraschung %']
            
            st.table(df)
            
            # Logik für "Heute"
            latest_earning = df.iloc[0]['Quartalsende']
            st.info(f"Letztes gemeldetes Quartal: {latest_earning}. Wenn heute Earnings sind, achte auf den 'Gemeldeten Gewinn' im Vergleich zur 'Erwartung'!")
        else:
            st.write("Keine Earnings-Daten gefunden.")

    with tab1:
        # (Hier bleibt dein bisheriger Analyse-Code mit KGV, Marge etc.)
        overview = get_json("OVERVIEW", SYMBOL)
        if "Symbol" in overview:
            st.metric("Marktkapitalisierung", f"${int(overview.get('MarketCapitalization', 0)):,}")
            st.write(f"**Sektor:** {overview.get('Sector')}")
            st.progress(float(overview.get('ProfitMargin', 0)), text="Gewinnmarge")

    with tab3:
        st.subheader("Live Markt-Sentiment")
        news = get_json("NEWS_SENTIMENT", SYMBOL)
        if "feed" in news:
            for n in news['feed'][:5]:
                st.write(f"🔹 **{n['overall_sentiment_label']}**: [{n['title']}]({n['url']})")
