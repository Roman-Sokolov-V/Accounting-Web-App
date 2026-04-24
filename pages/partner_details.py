from datetime import date, timedelta

import matplotlib.pyplot as plt
import streamlit as st

from db.crud import get_partner, get_partner_entries, get_partners
from db.engine import get_db
from pages.include.sidebar import get_sidebar

get_sidebar()
entries = None
query_params = st.query_params

if "partner_id" in query_params:
    partner_id = int(query_params["partner_id"])
    with get_db() as db:
        partner = get_partner(db=db, partner_id=partner_id)
        entries = get_partner_entries(db=db, partner_id=partner_id)
else:
    with get_db() as db:
        partners = get_partners(db)
        partner = st.selectbox(
            "partner *",
            options=partners,
            format_func=lambda partner: partner.name,
            placeholder="Choose a partner",
            index=None,
        )
        if partner:
            entries = get_partner_entries(db=db, partner_id=partner.id)


if entries:
    st.title(f"Details parner {partner.name}")

    st.caption("Balance is meaningful only in chronological order")
    balance = 0
    rows = []

    for e in entries:
        delta = e.debit - e.credit
        balance += delta
        rows.append(
            {
                "Entry date": e.date,
                "Account type": e.account.type,
                "Account name": e.account.name,
                "Debit": e.debit,
                "Credit": e.credit,
                "Balance": balance,
            }
        )

    st.dataframe(rows, use_container_width=True, hide_index=True)
    st.metric(
        label="Current balance", value=f"{balance:,.2f} ₴", delta=f"{delta:,.2f} ₴"
    )

    st.write("BALANCE CHART")
    today = date.today()
    delta_time = st.slider("Days", 0, len(rows) - 2 if len(rows) < 30 else 30)

    first_day = today - timedelta(days=delta_time)
    x = [str(first_day + timedelta(days=i)) for i in range(delta_time + 1)]

    y = [row.get("Balance") for row in rows][-delta_time - 2 : -1]

    fig, ax = plt.subplots()
    ax.bar(x, y)
    ax.tick_params(axis="both", which="major", labelsize=5)
    fig.autofmt_xdate(rotation=60)
    st.pyplot(fig)

else:
    st.warning("Please select a partner from the list.")
