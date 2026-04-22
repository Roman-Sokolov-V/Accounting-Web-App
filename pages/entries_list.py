import streamlit as st
from db.crud import get_all_entries
from db.engine import get_db

with st.sidebar:
    st.page_link("pages/transactions.py", label="Add transaction", icon="➕")
    st.page_link("pages/profit_loss.py", label="Profit & Loss", icon="📊")
    st.page_link("pages/partner_ledger.py", label="Partner ledger", icon="👥")
    st.page_link("pages/transactions_list.py", label="Transactions list", icon="📋")
    st.page_link("pages/entries_list.py", label="Entries list", icon="📋")

with get_db() as session:
    entries = get_all_entries(db=session)

entries_data = [
    {
        "ID": e.id,
        "Debit": e.debit,
        "Credit": e.credit,
        "Transaction_id": e.transaction_id,
        "Account name": e.account.name,
        "Account code": e.account.code,
    } for e in entries
]

st.dataframe(
    entries_data,
    use_container_width=True,
    hide_index=True
)
