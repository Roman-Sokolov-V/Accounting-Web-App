import streamlit as st
from db.crud import create_partner, get_partners
from db.engine import get_db
from db.models import DBPartners

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


st.write("Our partner ledger")
with get_db() as session:
    partners = get_partners(db=session)

partners_data = [
    {
        "ID": p.id,
        "Name": p.name,
        "Description": p.description
    } for p in partners
]

st.dataframe(
    partners_data,
    use_container_width=True,
    hide_index=True
)
