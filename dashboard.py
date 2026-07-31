import streamlit as st
import json
import urllib.request

# ─── LOCAL IP TESTING CONFIGURATION ───
# We leave this placeholder link here for your first launch.
# Once we deploy your backend to Render, we will swap this with your live server link.
API_URL = "http://127.0.0"

st.set_page_config(page_title="Poverty Scalper Console", layout="wide", page_icon="⚡")
st.title("⚡ Poverty Scalper: Dual-Market AI Command Center")

# Safe native network data fetcher
def secure_fetch_status(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            return json.loads(response.read().decode())
    except:
        return None

# Attempting connection to engine
status = secure_fetch_status(API_URL)

if status is None:
    st.error("Poverty Scalper Core Engine is offline. Please make sure your backend link is verified and awake.")
    st.stop()

# Splitting screen into two separate columns for multi-market view
col_crypto, col_forex = st.columns(2)

with col_crypto:
    st.header("🪙 Crypto Scalper Engine")
    is_crypto_live = status.get("crypto_active", False)
    st.metric(label="Crypto System Status", value="ACTIVE / RUNNING" if is_crypto_live else "IDLE / SECURED")
    st.info(f"Targeting Asset: `{status.get('crypto_asset', 'BTC/USDT')}`")
    
    if is_crypto_live:
        if st.button("🔴 DEACTIVATE CRYPTO BOT", use_container_width=True, key="btn_crypto_off"):
            try:
                urllib.request.urlopen(API_URL.replace("/status", "/toggle_crypto?status=false"), timeout=5)
                st.rerun()
            except: st.error("Failed to transmit command.")
    else:
        if st.button("🟢 ACTIVATE CRYPTO BOT", type="primary", use_container_width=True, key="btn_crypto_on"):
            try:
                urllib.request.urlopen(API_URL.replace("/status", "/toggle_crypto?status=true"), timeout=5)
                st.rerun()
            except: st.error("Failed to transmit command.")

with col_forex:
    st.header("💵 Forex Scalper Engine")
    is_forex_live = status.get("forex_active", False)
    st.metric(label="Forex System Status", value="ACTIVE / RUNNING" if is_forex_live else "IDLE / SECURED")
    st.info(f"Targeting Asset: `{status.get('forex_asset', 'EUR/USD')}`")
    
    if is_forex_live:
        if st.button("🔴 DEACTIVATE FOREX BOT", use_container_width=True, key="btn_forex_off"):
            try:
                urllib.request.urlopen(API_URL.replace("/status", "/toggle_forex?status=false"), timeout=5)
                st.rerun()
            except: st.error("Failed to transmit command.")
    else:
        if st.button("🟢 ACTIVATE FOREX BOT", type="primary", use_container_width=True, key="btn_forex_on"):
            try:
                urllib.request.urlopen(API_URL.replace("/status", "/toggle_forex?status=true"), timeout=5)
                st.rerun()
            except: st.error("Failed to transmit command.")

st.divider()
st.warning(f"⚠️ CAPITAL ALLOCATION LOCK: Global risk management constraint locked at maximum ${status.get('trade_allocation_usd', 10.0)} USD per trade block.")
