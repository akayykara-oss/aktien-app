import streamlit as st
import requests

# Seite für das iPhone optimieren
st.set_page_config(page_title="US Stock Analyzer", layout="centered")

# Dein API-Key und Konfiguration
API_KEY = "7WVP0MXARBW5EN7D"

st.title("🚀 US Aktien-Check")
st.write("Gib ein US-Kürzel ein, um eine Sofort-Analyse zu erhalten.")

# Eingabefeld
symbol = st.text_input("Ticker Symbol (z.B. NVDA, TSLA, AAPL)", "AAPL").upper()

def get_stock_overview(ticker):
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={API_KEY}"
    try:
        response = requests.get(url)
        return response.json()
    except:
        return None

if symbol:
    with st.spinner('Analysiere Markt-Daten...'):
        data = get_stock_overview(symbol)

    if data and "Symbol" in data:
        st.header(f"{data.get('Name', symbol)}")
        
        # Kennzahlen ziehen
        pe = float(data.get('PERatio', 0))
        div = float(data.get('DividendYield', 0)) * 100
        eps = data.get('EPS', 'N/A')

        # Mobile Anzeige in Kacheln
        col1, col2 = st.columns(2)
        col1.metric("KGV", pe)
        col2.metric("Dividende", f"{div:.2f}%")

        st.divider()

        # Ampel-Logik
        if pe > 0 and pe < 25:
            st.success("🟢 BEWERTUNG: Günstig / Fair (Kaufkandidat)")
        elif pe >= 25:
            st.warning("🟡 BEWERTUNG: Teuer (Vorsicht)")
        else:
            st.error("🔴 BEWERTUNG: Kein Gewinn / Risiko")

        # Beschreibung für den schnellen Überblick
        with st.expander("Was macht das Unternehmen?"):
            st.write(data.get('Description', 'Keine Beschreibung verfügbar.'))
    else:
        st.error("Limit erreicht oder Symbol falsch. Bitte 15 Sek. warten (Free API Key).")
