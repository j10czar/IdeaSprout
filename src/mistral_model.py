import sys
import requests
import json


def format_prompt_summary(text):
    return f"""
Given the following text, do three things:
1. Generate a clear and concise title summarizing the main idea.
2. Create a bullet-pointed summary of the key points.
3. List 5–10 keywords or tags related to the ideas in the text.

Text:
\"\"\"
{text.strip()}
\"\"\"
"""


def format_prompt_master(file_summaries):
    """
    file_summaries: List of dicts, each with keys: 'title', 'summary', 'keywords'
    """
    entries = []
    for idx, file in enumerate(file_summaries):
        title = file["title"]
        summary = file["summary"]
        keywords = ", ".join(file["keywords"])
        entries.append(
            f"{idx+1}. Title: {title}\nSummary:\n{summary}\nKeywords: {keywords}\n")

    joined = "\n\n".join(entries)

    return f"""
You are a markdown writer helping to organize topics for a mind map.

Given the following titles, summaries, and keywords from different documents, create a single master markdown outline that groups related ideas together. The goal is to make a mind map structure where:

- The broadest idea should be a top-level bullet.
- Sub-ideas go one indent deeper.
- If one idea is part of another, place it under that bullet.
- Use bullet points (`-`) and nested indents (`  -`, `    -`) to show the hierarchy.

Here is the data:
{joined}

Now output the markdown structure:
"""


def call_mistral(prompt):
    response = requests.post(
        'http://localhost:11434/api/generate',
        json={
            "model": "mistral:instruct",
            "prompt": prompt,
            "stream": False
        }
    )
    if response.status_code != 200:
        raise Exception(f"Failed: {response.status_code} {response.text}")

    return response.json()["response"]
