import streamlit as st
import requests

st.set_page_config(page_title="US Pro Trader", layout="wide")
API_KEY = "7WVP0MXARBW5EN7D"

st.title("🏛️ Professional US Equity Analyzer")

symbol = st.sidebar.text_input("Ticker Symbol", "NVDA").upper()

def get_data(func, sym):
    url = f"https://www.alphavantage.co/query?function={func}&symbol={sym}&apikey={API_KEY}"
    return requests.get(url).json()

if symbol:
    with st.spinner('Lade Profi-Daten...'):
        overview = get_data("OVERVIEW", symbol)
        # News Sentiment abrufen
        news = requests.get(f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={symbol}&apikey={API_KEY}").json()

    if "Symbol" in overview:
        # --- HEADER ---
        st.header(f"{overview['Name']} | {overview['Exchange']} | {overview['Sector']}")
        
        # --- KENNZAHLEN BLOCK ---
        col1, col2, col3, col4 = st.columns(4)
        pe = float(overview.get('PERatio', 0))
        profit_margin = float(overview.get('ProfitMargin', 0)) * 100
        rev_growth = float(overview.get('QuarterlyRevenueGrowthYOY', 0)) * 100
        target_price = overview.get('AnalystTargetPrice', 'N/A')

        col1.metric("KGV (P/E)", pe)
        col2.metric("Gewinnmarge", f"{profit_margin:.1f}%")
        col3.metric("Umsatzwachstum", f"{rev_growth:.1f}%")
        col4.metric("Analysten-Ziel", f"${target_price}")

        # --- AUTOMATISCHES SCORING ---
        st.subheader("🛡️ Investment Scorecard")
        score = 0
        checks = []
        
        if pe > 0 and pe < 20: score += 1; checks.append("✅ Bewertung: Attraktives KGV.")
        if profit_margin > 15: score += 1; checks.append("✅ Rentabilität: Starke Margen.")
        if rev_growth > 10: score += 1; checks.append("✅ Wachstum: Zweistelliges Wachstum.")
        
        c1, c2 = st.columns([1, 2])
        c1.progress(score / 3)
        c2.write(f"Gesamtscore: {score} von 3 Kriterien erfüllt.")

        # --- NEWS SENTIMENT ---
        st.subheader("📰 Aktuelle Marktstimmung")
        if "feed" in news:
            for item in news['feed'][:3]: # Zeige die Top 3 News
                sentiment = item.get('overall_sentiment_label', 'Neutral')
                st.write(f"**{sentiment}**: [{item['title']}]({item['url']})")
        else:
            st.write("Keine aktuellen News-Daten verfügbar.")

    else:
        st.error("Fehler beim Abrufen der Daten. Bitte Ticker prüfen oder 1 Minute warten.")
