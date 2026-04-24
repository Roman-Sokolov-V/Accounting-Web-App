import datetime
from decimal import Decimal

import streamlit as st

from db.crud import create_transaction_and_entries, get_partners
from db.engine import get_db
from db.models import TransactionsTypes
from pages.include.sidebar import get_sidebar

get_sidebar()

date = st.date_input(
    "select the date of the transaction, or leave the current", datetime.date.today()
)

type = st.selectbox(
    label="type *",
    options=list(TransactionsTypes),
    format_func=lambda x: x.value,
    placeholder="Choose a type",
    index=None,
)


with get_db() as session:
    partners = get_partners(db=session)

amount = Decimal(str(st.number_input("amount *", min_value=0.0, format="%.2f")))


partner = st.selectbox(
    "partner *",
    options=partners,
    format_func=lambda partner: partner.name,
    placeholder="Choose a partner",
    index=None,
)


description = st.text_input(
    "description", placeholder="Enter a description (not required)"
)

if type and amount and partner:
    if st.button("Add transaction"):
        try:
            with get_db() as session:
                create_transaction_and_entries(
                    db=session,
                    date=date,
                    type=type,
                    amount=amount,
                    partner_id=partner.id,
                    description=description,
                )
                session.commit()
            st.success("Transaction and entries saved successfully!")
        except Exception as e:
            st.error(f"Failed to save: {e}")
