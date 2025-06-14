import streamlit as st
import pandas as pd
import sqlite3
import os
from helpers.query_generator import generate_sql

st.set_page_config(page_title="AI HR Database Tool", layout="wide")

st.markdown("## 🧠 AI HR Database Tool")

# Sidebar Navigation
st.sidebar.title("Navigation")
mode = st.sidebar.selectbox("Choose a mode", ["Run Query"])

# --- File Upload Section ---
st.sidebar.markdown("### 📂 Upload File")
uploaded_file = st.sidebar.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

# Track current table
if uploaded_file:
    file_ext = os.path.splitext(uploaded_file.name)[1]
    if file_ext == ".csv":
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.session_state["df"] = df
    st.session_state["table_name"] = "uploaded_data"

    # Load into SQLite in-memory DB
    conn = sqlite3.connect(":memory:")
    df.to_sql(st.session_state["table_name"], conn, index=False, if_exists="replace")

    st.sidebar.success(f"✅ {uploaded_file.name} uploaded successfully!")

    st.dataframe(df.head(), use_container_width=True)

# --- Main App Logic ---
if mode == "Run Query":
    st.header("💬 Run Your Query")
    prompt = st.text_area("Please enter your question (e.g. show all employees in HR department):")

    if st.button("Submit Query") and prompt:
        if "df" not in st.session_state:
            st.error("Please upload a CSV or Excel file first.")
        else:
            # 👇 Send to Groq + LLaMA3 and get SQL
            sql = generate_sql(prompt, st.session_state["df"].columns.tolist(), st.session_state["table_name"])

            st.success("🧠 SQL Query Generated")
            st.code(sql, language="sql")

            # Run SQL on uploaded table
            try:
                result_df = pd.read_sql_query(sql, conn)
                st.subheader("📊 Query Results")
                st.dataframe(result_df, use_container_width=True)
            except Exception as e:
                st.error(f"❌ Error\n\n{str(e)}")








