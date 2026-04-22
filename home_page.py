import streamlit as st

st.write("💰CASH")
st.write("📈Profit")
st.write("🧾Outstanding receivables")
st.write("💳Payables")
with st.sidebar:
    st.page_link("pages/transactions.py", label="Add transaction", icon="➕")
    st.page_link("pages/profit_loss.py", label="Profit & Loss", icon="📊")
    st.page_link("pages/partner_ledger.py", label="Partner ledger", icon="👥")
    st.page_link("pages/transactions_list.py", label="Transactions list", icon="📋")