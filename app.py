import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import date

# ---------- Config ----------
st.set_page_config(page_title="Student Expense Tracker", page_icon="💸", layout="wide")
CSV_FILE = "expenses.csv"

# ---------- Load / Save ----------
def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    return pd.DataFrame(columns=["Date", "Category", "Description", "Amount"])

def save_data(df):
    df.to_csv(CSV_FILE, index=False)

# ---------- Main App ----------
st.title("💸 BUDGET TRACKER FOR AITM STUDENTS")
st.caption("Track your daily spending — built with Python & Streamlit")

df = load_data()

# --- Add Expense Form ---
st.subheader("➕ Add New Expense")

col1, col2 = st.columns(2)
with col1:
    exp_date = st.date_input("Date", value=date.today())
    category = st.selectbox("Category", ["Food", "Transport", "Books", "Entertainment", "Health","recharge","donation", "Other"])
with col2:
    description = st.text_input("Description", placeholder="e.g. Lunch at canteen")
    amount = st.number_input("Amount ($)", min_value=0.0, step=10.0)

if st.button("Add Expense", use_container_width=True):
    if amount > 0 and description:
        new_row = {"Date": str(exp_date), "Category": category, "Description": description, "Amount": amount}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        save_data(df)
        st.success(f"✅ Added ₹{amount} for {description}")
        st.rerun()
    else:
        st.warning("Please enter a description and amount greater than 0.")

st.divider()

# --- Summary ---
if not df.empty:
    st.subheader("📊 Your Spending Summary")

    total = df["Amount"].sum()
    st.metric("Total Spent", f"₹{total:,.2f}")

    col3, col4 = st.columns(2)

    with col3:
        # Pie chart
        cat_summary = df.groupby("Category")["Amount"].sum().reset_index()
        fig = px.pie(cat_summary, names="Category", values="Amount", title="Spending by Category")
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        # Bar chart
        df["Date"] = pd.to_datetime(df["Date"])
        daily = df.groupby("Date")["Amount"].sum().reset_index()
        fig2 = px.bar(daily, x="Date", y="Amount", title="Daily Spending")
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("📋 All Expenses")
    st.dataframe(df.sort_values("Date", ascending=False), use_container_width=True)

    # Delete option
    st.subheader("🗑️ Delete an Expense")
    if len(df) > 0:
        index_to_delete = st.selectbox("Select row to delete", df.index, format_func=lambda x: f"{df.loc[x,'Date'].date()} | {df.loc[x,'Category']} | ₹{df.loc[x,'Amount']} | {df.loc[x,'Description']}")
        if st.button("Delete Selected", use_container_width=True):
            df = df.drop(index=index_to_delete).reset_index(drop=True)
            save_data(df)
            st.success("Deleted!")
            st.rerun()
else:
    st.info("No expenses yet. Add your first one above! 👆")