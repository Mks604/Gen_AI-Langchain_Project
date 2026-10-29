
import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Get the OpenRouter API key
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["OPENROUTER_API_KEY"]
    except (KeyError, FileNotFoundError):
        api_key = None

if not api_key:
    raise RuntimeError(
        "OPENROUTER_API_KEY is missing. "
        "Add it to Streamlit Community Cloud Secrets."
    )

# OpenRouter uses the OpenAI-compatible API
client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1",
)

# Automatically routes to an available free model
MODEL = "openrouter/free"


def generate_code(prompt):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful Python coding assistant. "
                    "Generate accurate, readable code with explanations "
                    "when useful."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )

    return response.choices[0].message.content or ""


def explain_code(code):
    prompt = f"Explain the following code in simple terms:\n{code}"
    return generate_code(prompt)


def fix_code(code):
    prompt = (
        "Find and fix bugs in the following code. "
        "Return the corrected code and explain the changes:\n"
        f"{code}"
    )
    return generate_code(prompt)
