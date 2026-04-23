from datetime import date, timedelta
import matplotlib.pyplot as plt
import streamlit as st
from db.crud import get_partner, get_partner_entries
from db.engine import get_db
from pages.include.sidebar import get_sidebar

get_sidebar()

query_params = st.query_params

if "partner_id" in query_params:
    p_id = int(query_params["partner_id"])
    with get_db() as session:
        partner = get_partner(session, partner_id=p_id)
        entries = get_partner_entries(db=session, partner_id=p_id)

    st.title(f"Details parner {partner. name}")


    st.caption("Balance is meaningful only in chronological order")
    balance = 0
    rows = []

    for e in entries:
        delta = e.debit - e.credit
        balance += delta
        rows.append({
            "Entry date": e.date,
            "Account type": e.account.type,
            "Account name": e.account.name,
            "Debit": e.debit,
            "Credit": e.credit,
            "Balance": balance
    })

    st.dataframe(
        rows,
        use_container_width=True,
        hide_index=True
    )
    st.metric(
        label="Current balance",
        value=f"{balance:,.2f} ₴",
        delta=f"{delta:,.2f} ₴"
    )

    st.write("BALANCE CHART")
    today = date.today()
    delta_time = st.slider("Days", 0, len(rows) - 2)

    first_day = today - timedelta(days=delta_time)
    x = [str(first_day + timedelta(days=i)) for i in range(delta_time + 1)]

    y = [row.get("Balance") for row in rows][-delta_time - 2: -1]

    fig, ax = plt.subplots()
    ax. bar(x, y)

    fig.autofmt_xdate()
    st.pyplot(fig)

else:
    st.warning("Please select a partner from the list.")