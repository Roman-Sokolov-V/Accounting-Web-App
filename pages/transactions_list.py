import streamlit as st
from db.crud import get_all_transactions
from db.engine import get_db

with st.sidebar:
    st.page_link("pages/transactions.py", label="Add transaction", icon="➕")
    st.page_link("pages/profit_loss.py", label="Profit & Loss", icon="📊")
    st.page_link("pages/partner_ledger.py", label="Partner ledger", icon="👥")
    st.page_link("pages/transactions_list.py", label="Transactions list", icon="📋")
    st.page_link("pages/entries_list.py", label="Entries list")

with get_db() as session:
    transactions = get_all_transactions(db=session)

transactions_data = [
    {
        "ID": t.id,
        "Type": t.type.name,
        "Amount": t.amount,
        "Partner ID": t.partner_id,
        "Entries IDs": " | ".join([
            f"{e.id}"
            for e in t.entries
        ]),
        "Description": t.description
    } for t in transactions
]

st.dataframe(
    transactions_data,
    use_container_width=True,
    hide_index=True
)
