import streamlit as st
import requests
import pandas as pd

# KONFIGURATION
API_KEY = "DEIN_API_KEY_HIER"  # Ersetze dies durch deinen Key
SYMBOL = st.sidebar.text_input("Ticker Symbol (z.B. AAPL, TSLA)", "AAPL")

def get_stock_data(symbol):
    # Fundamentaldaten abrufen
    url = f"https://financialmodelingprep.com/api/v3/key-metrics-ttm/{symbol}?apikey={API_KEY}"
    data = requests.get(url).json()
    return data[0] if data else None

st.title(f"🚀 AI Stock Analyzer: {SYMBOL}")

data = get_stock_data(SYMBOL)

if data:
    # Kennzahlen extrahieren
    pe_ratio = data.get('peRatioTTM', 0)
    debt_to_equity = data.get('debtToEquityTTM', 0)
    roe = data.get('roeTTM', 0) * 100 # In Prozent

    # AUTOMATISCHE ANALYSE (Scoring 0-3)
    score = 0
    reasons = []

    if pe_ratio < 20: 
        score += 1
        reasons.append("✅ Günstig bewertet (KGV < 20)")
    if roe > 15: 
        score += 1
        reasons.append("✅ Hohe Eigenkapitalrendite (> 15%)")
    if debt_to_equity < 1: 
        score += 1
        reasons.append("✅ Solide Finanzen (Verschuldung < 1)")

    # ANZEIGE
    col1, col2, col3 = st.columns(3)
    col1.metric("KGV", f"{pe_ratio:.2f}")
    col2.metric("ROE", f"{roe:.2f}%")
    col3.metric("Debt/Equity", f"{debt_to_equity:.2f}")

    st.subheader(f"Gesamt-Score: {score} / 3")
    for r in reasons:
        st.write(r)

    if score >= 2:
        st.success("EMPFEHLUNG: KAUFEN / HALTEN")
    else:
        st.error("EMPFEHLUNG: VORSICHT / VERKAUFEN")
else:
    st.warning("Keine Daten gefunden. Überprüfe das Symbol oder den API-Key.")import streamlit as st
import requests
import pandas as pd

# KONFIGURATION
API_KEY = "DEIN_API_KEY_HIER"  # Ersetze dies durch deinen Key
SYMBOL = st.sidebar.text_input("Ticker Symbol (z.B. AAPL, TSLA)", "AAPL")

def get_stock_data(symbol):
    # Fundamentaldaten abrufen
    url = f"https://financialmodelingprep.com/api/v3/key-metrics-ttm/{symbol}?apikey={API_KEY}"
    data = requests.get(url).json()
    return data[0] if data else None

st.title(f"🚀 AI Stock Analyzer: {SYMBOL}")

data = get_stock_data(SYMBOL)

if data:
    # Kennzahlen extrahieren
    pe_ratio = data.get('peRatioTTM', 0)
    debt_to_equity = data.get('debtToEquityTTM', 0)
    roe = data.get('roeTTM', 0) * 100 # In Prozent

    # AUTOMATISCHE ANALYSE (Scoring 0-3)
    score = 0
    reasons = []

    if pe_ratio < 20: 
        score += 1
        reasons.append("✅ Günstig bewertet (KGV < 20)")
    if roe > 15: 
        score += 1
        reasons.append("✅ Hohe Eigenkapitalrendite (> 15%)")
    if debt_to_equity < 1: 
        score += 1
        reasons.append("✅ Solide Finanzen (Verschuldung < 1)")

    # ANZEIGE
    col1, col2, col3 = st.columns(3)
    col1.metric("KGV", f"{pe_ratio:.2f}")
    col2.metric("ROE", f"{roe:.2f}%")
    col3.metric("Debt/Equity", f"{debt_to_equity:.2f}")

    st.subheader(f"Gesamt-Score: {score} / 3")
    for r in reasons:
        st.write(r)

    if score >= 2:
        st.success("EMPFEHLUNG: KAUFEN / HALTEN")
    else:
        st.error("EMPFEHLUNG: VORSICHT / VERKAUFEN")
else:
    st.warning("Keine Daten gefunden. Überprüfe das Symbol oder den API-Key.")