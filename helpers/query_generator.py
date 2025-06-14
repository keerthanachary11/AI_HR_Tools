import httpx
import os
import re

GROQ_API_KEY = "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"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


def extract_sql(text):
    match = re.search(r"```sql(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()

    match = re.search(r"(SELECT .*?);", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()

    return "-- ERROR: No SQL query found in response --"

def generate_sql(prompt, columns, table_name="uploaded_data"):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    columns_str = ", ".join(columns)

    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {
                "role": "system",
                "content": (
                    f"You are a helpful assistant that only returns SQL queries for a table named '{table_name}' "
                    f"with columns: {columns_str}. Only return the SQL query without explanation."
                )
            },
            {"role": "user", "content": prompt}
        ]
    }

    response = httpx.post(GROQ_URL, headers=headers, json=data)
    response_json = response.json()

    if "choices" in response_json:
        return extract_sql(response_json["choices"][0]["message"]["content"])
    elif "error" in response_json:
        return f"-- ERROR: {response_json['error']['message']} --"
    else:
        return "-- ERROR: Unexpected response format --"
