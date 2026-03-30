from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

messages = [
    {"role":"system","content": "You are Someone who knows everything. keep answering everything short and clear"}
]

print("======Chatbot======")
print("Type 'quit' to exit\n")

while True:
    user_input = input("You: ").strip()

    if not user_input:
        continue
    if user_input.lower() == "quit":
        print("Bye!")
        break

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=messages
    )

    reply =  (response.choices[0].message.content)

    messages.append({"role": "assistant", "content": reply})

    print(f"\nAi: {reply}\n")