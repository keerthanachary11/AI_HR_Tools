import httpx
import os

GROQ_API_KEY = "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"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def generate_sql(natural_query):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an AI that converts natural language queries into valid SQLite SQL queries. "
                    "Assume the employee database schema is: employees(id, name, department, designation, salary, location, hire_date)."
                )
            },
            {"role": "user", "content": natural_query}
        ]
    }

    try:
        response = httpx.post(GROQ_URL, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    except httpx.HTTPStatusError as e:
        print(f"❌ HTTP error from Groq API: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

    return None

