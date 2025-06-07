import streamlit as st
import sqlite3
import pandas as pd
from helpers.query_generator import generate_sql

def extract_sql(query_text):
    """
    Extracts only the actual SQL statement from the model's output.
    Stops at the first semicolon or before any explanations.
    """
    # Remove any markdown code block markers and strip whitespace
    cleaned = query_text.replace("```sql", "").replace("```", "").strip()
    lines = cleaned.splitlines()
    sql_lines = []
    recording = False

    for line in lines:
        line_strip = line.strip()
        # Skip empty lines or comments
        if not line_strip or line_strip.startswith("--"):
            continue

        # Start recording when the first SQL keyword is detected
        if not recording and line_strip.upper().startswith(("SELECT", "WITH", "INSERT", "UPDATE", "DELETE")):
            recording = True

        if recording:
            # Stop recording if explanation or note starts
            if line_strip.upper().startswith(("EXPLANATION", "NOTE", "COMMENT", "THIS QUERY")):
                break
            sql_lines.append(line)
            if ";" in line_strip:
                break

    final_sql = "\n".join(sql_lines).strip()
    # Ensure the SQL statement ends with semicolon
    if ";" in final_sql:
        final_sql = final_sql.split(";")[0] + ";"

    return final_sql

st.set_page_config(page_title="AI HR Database Tool", layout="wide")

st.sidebar.markdown("### Navigation")
mode = st.sidebar.selectbox("Choose a mode", ["Run Query"])

if mode == "Run Query":
    st.markdown("<h1 style='text-align: center; color: white;'>Run Your Query</h1>", unsafe_allow_html=True)
    st.caption("Please enter your question (e.g. *show all employees in HR department*):")
    user_input = st.text_area("", placeholder="e.g. show all employees in Tech department", height=100)

    if st.button("Submit Query", type="primary"):
        if user_input.strip():
            with st.spinner("Generating SQL..."):
                try:
                    raw_sql_query = generate_sql(user_input)
                    sql_query = extract_sql(raw_sql_query)
                except Exception as e:
                    st.error(f"❌ Failed to generate SQL: {e}")
                    st.stop()

            st.markdown("### 🔍 SQL Query Generated")
            st.code(sql_query, language="sql")

            try:
                with sqlite3.connect("employees.db") as conn:
                    df = pd.read_sql_query(sql_query, conn)
                    st.markdown("### 📊 Query Results")
                    if not df.empty:
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.warning("⚠️ No results found.")
            except Exception as e:
                st.error("❌ SQL Execution Error:")
                st.code(str(e))
        else:
            st.warning("⚠️ Please enter a question first!")
