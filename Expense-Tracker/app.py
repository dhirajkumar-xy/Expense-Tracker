import io

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Expense Tracker", layout="wide")
st.title("💰 Expense Tracker with Visuals")

CATEGORIES = ["Food", "Travel", "Bills", "Shopping", "Health", "Education", "Other"]
COLUMNS = ["date", "category", "description", "amount"]

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=COLUMNS)


def clean(df):
    """Clean the data and fix categories."""
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()
    if "description" not in df:
        df["description"] = ""
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df["category"] = df["category"].astype(str).str.strip().str.title()
    df = df.dropna(subset=["date", "amount"]).drop_duplicates()
    return df[COLUMNS]


# ---------- Sidebar ----------
with st.sidebar:
    st.header("Add expense")
    with st.form("add_form", clear_on_submit=True):
        d = st.date_input("Date")
        cat = st.selectbox("Category", CATEGORIES)
        desc = st.text_input("Description")
        amt = st.number_input("Amount (₹)", min_value=0.0, step=10.0)
        if st.form_submit_button("Add"):
            row = pd.DataFrame([[d, cat, desc, amt]], columns=COLUMNS)
            st.session_state.df = clean(pd.concat([st.session_state.df, row]))

    st.header("Or upload CSV")
    file = st.file_uploader("CSV (date, category, description, amount)", type="csv")
    if file and st.button("Load CSV"):
        new = clean(pd.read_csv(file))
        st.session_state.df = clean(pd.concat([st.session_state.df, new]))
        st.success(f"Loaded {len(new)} rows!")

    st.header("Budget")
    budget = st.number_input("Total budget (₹)", min_value=0.0, value=40000.0, step=500.0)

    if st.button("Clear All Data"):
        st.session_state.df = pd.DataFrame(columns=COLUMNS)
        st.rerun()

df = st.session_state.df
if df.empty:
    st.info("Sidebar se expense add karo ya CSV upload karo.")
    st.stop()

# ---------- Filters ----------
f1, f2 = st.columns(2)
date_range = f1.date_input(
    "Filter by date", (df["date"].min().date(), df["date"].max().date())
)
all_cats = sorted(df["category"].unique())
cats = f2.multiselect("Filter by category", all_cats, default=all_cats)

if len(date_range) != 2:
    st.info("Date range ke liye start aur end dono date chuno.")
    st.stop()

start, end = date_range
mask = (
    (df["date"].dt.date >= start)
    & (df["date"].dt.date <= end)
    & (df["category"].isin(cats))
)
fdf = df[mask]
if fdf.empty:
    st.warning("Is filter me koi expense nahi mila.")
    st.stop()

# ---------- Summary ----------
total = fdf["amount"].sum()
c1, c2, c3 = st.columns(3)
c1.metric("Total Spent", f"₹{total:,.0f}")
c2.metric("Average expense", f"₹{fdf['amount'].mean():,.0f}")
c3.metric("Entries", len(fdf))

# ---------- Budget alert ----------
if total > budget:
    st.error(f"⚠️ Budget cross ho gaya! Limit ₹{budget:,.0f}, kharch ₹{total:,.0f}")
elif total > 0.8 * budget:
    st.warning(f"Budget ka 80% se zyada use ho gaya (₹{total:,.0f} / ₹{budget:,.0f})")
else:
    st.success(f"Budget theek hai (₹{total:,.0f} / ₹{budget:,.0f})")

# ---------- Grouping ----------
by_cat = fdf.groupby("category")["amount"].sum().sort_values(ascending=False)
by_month = fdf.groupby(fdf["date"].dt.to_period("M").astype(str))["amount"].sum()

# ---------- Charts ----------
left, right = st.columns(2)
with left:
    st.subheader("By Category")
    fig, ax = plt.subplots()
    ax.pie(by_cat, labels=by_cat.index, autopct="%1.1f%%", startangle=90)
    st.pyplot(fig)
with right:
    st.subheader("Monthly Trend")
    fig, ax = plt.subplots()
    by_month.plot(kind="bar", ax=ax, color="teal")
    ax.set_xlabel("Month")
    ax.set_ylabel("Amount (₹)")
    plt.xticks(rotation=45)
    st.pyplot(fig)

st.subheader("All expenses")
st.dataframe(fdf.sort_values("date", ascending=False), use_container_width=True)

# ---------- Export to Excel ----------
buf = io.BytesIO()
with pd.ExcelWriter(buf, engine="openpyxl") as writer:
    out = fdf.copy()
    out["date"] = out["date"].dt.date
    out.to_excel(writer, sheet_name="Expenses", index=False)
    by_cat.to_frame("total").to_excel(writer, sheet_name="By Category")
    by_month.to_frame("total").to_excel(writer, sheet_name="By Month")
    for ws in writer.book.worksheets:
        for col in ws.columns:
            ws.column_dimensions[col[0].column_letter].width = 18
st.download_button(
    "📥 Export report to Excel",
    buf.getvalue(),
    file_name="expense_report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)