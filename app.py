import streamlit as st
import sqlite3
import pandas as pd
from helpers.query_generator import generate_sql

# === Improved Extract SQL Function ===
def extract_sql(query_text):
    """
    Extracts only the actual SQL statement (single statement).
    It stops at any non-SQL line (like comments or explanations).
    """
    cleaned = query_text.replace("```sql", "").replace("```", "").strip()
    lines = cleaned.splitlines()
    sql_lines = []

    for line in lines:
        # Skip empty or comment lines
        if not line.strip() or line.strip().startswith("--"):
            continue
        # Skip explanations before SQL begins
        if not line.strip().upper().startswith(("SELECT", "WITH", "INSERT", "UPDATE", "DELETE")) and not sql_lines:
            continue
        # Stop if an explanation is encountered after SQL
        if sql_lines and not any(keyword in line.upper() for keyword in ("SELECT", "WITH", "INSERT", "UPDATE", "DELETE")):
            break
        sql_lines.append(line)

    return "\n".join(sql_lines).strip()

# === UI Settings ===
st.set_page_config(page_title="AI HR Database Tool", layout="wide")

# === Sidebar Navigation ===
st.sidebar.markdown("### Navigation")
mode = st.sidebar.selectbox("Choose a mode", ["Run Query"])

if mode == "Run Query":
    # Updated heading color to white
    st.markdown("<h1 style='text-align: center; color: white;'>Run Your Query</h1>", unsafe_allow_html=True)
    st.caption("Please enter your query:")

    # Input Area
    user_input = st.text_area("", placeholder="e.g. show all the employees in Tech department", height=100)

    # Query Button
    if st.button("Submit Query", type="primary"):
        if user_input.strip():  # Only process if there is input
            with st.spinner("Generating SQL..."):
                raw_sql_query = generate_sql(user_input)
                sql_query = extract_sql(raw_sql_query)

            # Display the extracted SQL
            st.markdown("### SQL Query")
            st.code(sql_query, language="sql")

            # Execute and display result
            try:
                with sqlite3.connect("employees.db") as conn:
                    df = pd.read_sql_query(sql_query, conn)
                    st.markdown("### Query Results")
                    if not df.empty:
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.warning("⚠️ No results found.")
            except Exception as e:
                st.error(f"❌ Error executing SQL: {e}")
        else:
            st.warning("⚠️ Please enter a query first!")


