import streamlit as st
from db.crud import get_all_entries
from db.engine import get_db
from pages.include.sidebar import get_sidebar

get_sidebar()

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
