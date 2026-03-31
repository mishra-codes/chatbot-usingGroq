from groq import Groq
from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
tavily_client= TavilyClient(api_key=os.getenv("TAVILY_API_KEy"))

def search_web(query):
    results = tavily_client.search(query, max_results=3)
    
    search_data = ""
    for result in results["results"]:
        search_data += f"Source: {result['url']}\n"
        search_data += f"Content: {result['content']}\n\n"
    return search_data



messages = [
    {"role":"system","content": """"You are a helpful assistant with web search ability.
     When answering, use the search results provided to give accurate up to date answers.
     Always mention where you got the information from."""}
]

print("======Chatbot with Web Search======")
print("Type 'quit' to exit\n")

while True:
    user_input = input("You: ").strip()

    if not user_input:
        continue
    if user_input.lower() == "quit":
        print("Bye!")
        break


        print("🔍 Searching web...")
    search_results = search_web(user_input)

    # Add search results + user question together
    combined = f"""User question: {user_input}

Here are relevant search results:
{search_results}

Answer the question using these search results."""

    messages.append({"role": "user", "content": combined})

    response = groq_client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=messages
    )

    reply =  (response.choices[0].message.content)

    messages.append({"role": "assistant", "content": reply})

    print(f"\nAI: {reply}\n")