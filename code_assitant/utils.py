
import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Read the API key from the environment or Streamlit Secrets.
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
    except (KeyError, FileNotFoundError):
        api_key = None

if not api_key:
    raise RuntimeError(
        "OPENAI_API_KEY is missing. "
        "Configure it in Streamlit Community Cloud Secrets."
    )

client = OpenAI(api_key=api_key)


def generate_code(prompt):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful coding assistant.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )

    return response.choices[0].message.content


def explain_code(code):
    prompt = f"Explain the following code in simple terms:\n{code}"
    return generate_code(prompt)


def fix_code(code):
    prompt = f"Fix bugs in the following code:\n{code}"
    return generate_code(prompt)
