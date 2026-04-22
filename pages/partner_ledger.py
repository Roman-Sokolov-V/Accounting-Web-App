import streamlit as st
from db.crud import create_partner
from db.engine import get_db

with st.sidebar:
    st.page_link("pages/transactions.py", label="Add transaction", icon="➕")
    st.page_link("pages/profit_loss.py", label="Profit & Loss", icon="📊")
    st.page_link("pages/partner_ledger.py", label="Partner ledger", icon="👥")
    st.page_link("pages/transactions_list.py", label="Transactions list", icon="📋")

st.write("Add new partner")
name = st.text_input("name", placeholder="Enter a description (required)")
description = st.text_input("description", placeholder="Enter a description (not required)")

if name:
    if st.button("Add partner"):
        with get_db() as session:
            create_partner(db=session, name=name, description=description)
        st.write ("New partner is added to database")
