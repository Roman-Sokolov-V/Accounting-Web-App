import streamlit as st

def get_sidebar():
    with st.sidebar:
        st.page_link("pages/transactions.py", label="Add transaction", icon="➕")
        st.page_link("profit_loss.py", label="Profit & Loss", icon="📊")
        st.page_link("pages/partner_ledger.py", label="Partner ledger", icon="👥")
        st.page_link("pages/transactions_list.py", label="Transactions list", icon="📋")
        st.page_link("pages/entries_list.py", label="Entries list")