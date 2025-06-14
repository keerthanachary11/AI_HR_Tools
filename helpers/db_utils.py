import sqlite3
import pandas as pd

def run_query(query):
    conn = sqlite3.connect("employees.db")
    try:
        df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        return pd.DataFrame({"Error": [str(e)]})
    finally:
        conn.close()
