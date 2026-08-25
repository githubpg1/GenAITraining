import csv
import os
import re

import requests
from dotenv import load_dotenv

from config import (
    MODEL,
    OPENROUTER_URL,
    CLIENT_NAME,
    TEMPERATURE
)


# ---------------------------------------------------------
# Load API key
# ---------------------------------------------------------

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    raise ValueError("OPENROUTER_API_KEY is missing from .env")


# ---------------------------------------------------------
# Read account activity
# ---------------------------------------------------------

def load_activity(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return list(csv.DictReader(file))


# ---------------------------------------------------------
# Convert CSV data into text for the LLM
# ---------------------------------------------------------

def format_activity(rows):
    lines = []

    for row in rows:
        lines.append(
            f"Date: {row['date']} | "
            f"Event: {row['event']} | "
            f"Amount: {row['amount']} | "
            f"Balance: {row['balance']}"
        )

    return "\n".join(lines)


# ---------------------------------------------------------
# System prompt
# ---------------------------------------------------------

SYSTEM_PROMPT = """
You are a relationship manager writing a monthly account review
for a named client.

Rules:

1. Use ONLY figures, dates, events, balances and products explicitly
   present in the supplied account activity.

2. Do not invent amounts, dates, events, products or explanations.

3. Do not assume why a transaction occurred.

4. If the source does not explain something, say that the available
   information does not provide that detail.

5. Do not recommend trades.

6. Do not promise returns.

7. Do not recommend or invent financial products.

8. Write exactly TWO paragraphs.

9. Do not use bullet points.

10. Do not reproduce the entire account statement.

11. Write professionally as a relationship manager speaking to
    the named client.

12. Do not add a heading.

Return only the two paragraphs.
"""


# ---------------------------------------------------------
# Call the LLM
# ---------------------------------------------------------

def generate_review(activity_text):

    user_prompt = f"""
Client: {CLIENT_NAME}

Account activity:

{activity_text}

Write the two-paragraph client review according to the rules.
"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "temperature": TEMPERATURE,
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    }

    response = requests.post(
        OPENROUTER_URL,
        headers=headers,
        json=payload,
        timeout=60
    )

    response.raise_for_status()

    data = response.json()

    return data["choices"][0]["message"]["content"].strip()


# ---------------------------------------------------------
# Number normalization
# ---------------------------------------------------------

def normalize_number(value):
    return (
        value
        .replace("₹", "")
        .replace(",", "")
        .replace("+", "")
        .replace("-", "")
        .strip()
    )


# ---------------------------------------------------------
# Get amounts from source
# ---------------------------------------------------------

def get_source_amounts(rows):

    amounts = set()

    for row in rows:
        amounts.add(normalize_number(row["amount"]))
        amounts.add(normalize_number(row["balance"]))

    return amounts


# ---------------------------------------------------------
# Get amounts from generated review
# ---------------------------------------------------------

def get_draft_amounts(text):

    # Finds numbers such as:
    # ₹250,000
    # 250,000
    # 250000

    pattern = r"₹?\s?\d[\d,]*(?:\.\d+)?"

    matches = re.findall(pattern, text)

    return {
        normalize_number(value)
        for value in matches
    }


# ---------------------------------------------------------
# Fact check amounts
# ---------------------------------------------------------

def fact_check_amounts(draft, rows):

    source_amounts = get_source_amounts(rows)
    draft_amounts = get_draft_amounts(draft)

    print("\nFACT CHECK")
    print("-" * 40)

    passed = True

    for amount in sorted(draft_amounts):

        if amount in source_amounts:
            print(f"{amount} → IN SOURCE")
        else:
            print(f"{amount} → NOT IN SOURCE")
            passed = False

    return passed


# ---------------------------------------------------------
# Check two paragraphs
# ---------------------------------------------------------

def has_two_paragraphs(text):

    paragraphs = [
        p.strip()
        for p in re.split(r"\n\s*\n", text)
        if p.strip()
    ]

    return len(paragraphs) == 2


# ---------------------------------------------------------
# Main program
# ---------------------------------------------------------

def main():

    print("=" * 60)
    print("RELATIONSHIP MANAGER REVIEW")
    print("=" * 60)

    # 1. Read source data
    rows = load_activity("account_activity.csv")

    # 2. Convert source data to text
    activity_text = format_activity(rows)

    # 3. Generate review
    review = generate_review(activity_text)

    # 4. Print review
    print("\n" + review)

    # 5. Check paragraph requirement
    paragraph_check = has_two_paragraphs(review)

    # 6. Check factual amounts
    fact_check = fact_check_amounts(review, rows)

    # 7. Final decision
    print("\n" + "-" * 40)

    if paragraph_check:
        print("Two paragraphs → PASS")
    else:
        print("Two paragraphs → FAIL")

    if paragraph_check and fact_check:
        print("Would I send this draft as-is? YES")
    else:
        print("Would I send this draft as-is? NO")


if __name__ == "__main__":
    main()