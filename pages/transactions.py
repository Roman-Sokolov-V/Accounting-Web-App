from decimal import Decimal
import streamlit as st

from  db.models import TransactionsTypes
from db.crud import get_partners, create_transaction_and_entries
from db.engine import get_db

with st.sidebar:
    st.page_link("pages/transactions.py", label="Add transaction", icon="➕")
    st.page_link("pages/profit_loss.py", label="Profit & Loss", icon="📊")
    st.page_link("pages/partner_ledger.py", label="Partner ledger", icon="👥")
    st.page_link("pages/transactions_list.py", label="Transactions list", icon="📋")


type = st.selectbox(
    label="type *",
    options=list(TransactionsTypes),
    format_func=lambda x: x.value,
    placeholder="Choose a type",
    index=None
)

st.write(type)

with get_db() as session:
    partners = get_partners(db=session)

amount = Decimal(str(st.number_input("amount *", min_value=0.0, format="%.2f")))
st.write(amount)

partner = st.selectbox(
    "partner *",
    options=partners,
    format_func=lambda partner: partner.name,
    placeholder="Choose a partner",
    index=None
)

st.write(partner)

description = st.text_input("description", placeholder="Enter a description (not required)")

if type and amount and partner:
    if st.button("Add transaction"):
        try:
            with get_db() as session:
                create_transaction_and_entries(
                    db=session,
                    type=type,
                    amount=amount,
                    partner_id=partner.id,
                    description=description
                )
            st.success("Transaction and entries saved successfully!")
        except Exception as e:
            st.error(f"Failed to save: {e}")