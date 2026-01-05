import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("HF_API_TOKEN")
if not API_TOKEN:
    print("❌ API token not found")
    exit()

API_URL = "https://router.huggingface.co/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

def text_with_assignment(topic):
    prompt = f"""
Explain the topic "{topic}" clearly in simple English.

After the explanation, create an **Assignment Section** with:
- 5 questions
- Questions should be based ONLY on this topic
- Mix of short answer and descriptive questions
- Suitable for students

Use clear headings:
1. Explanation
2. Assignment Questions
"""

    payload = {
        "model": "meta-llama/Meta-Llama-3-8B-Instruct",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a helpful teacher. "
                    "Explain topics clearly and then create assignment questions."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 500,
        "temperature": 0.6
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)

    if response.status_code != 200:
        return f"❌ HTTP {response.status_code}: {response.text}"

    data = response.json()
    return data["choices"][0]["message"]["content"]

# -------- MAIN LOOP --------
print("🔹 Enter a topic (type 'exit' to quit)")

while True:
    user_input = input("\nUser: ").strip()

    if user_input.lower() == "exit":
        print("👋 Exiting program. Goodbye!")
        break

    if not user_input:
        print("⚠️ Please enter a topic.")
        continue

    output = text_with_assignment(user_input)
    print("\n📘 Output:\n")
    print(output)
