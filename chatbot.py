from groq import Groq
from tavily import TavilyClient #tavilly is used for web search
import os
import json
from dotenv import load_dotenv

load_dotenv()

#initializing clients
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
tavily_client= TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

#Define the search tool- tells the ai which tool is available
tools = [
    {
        "type": "function",
        "function": {
            "name":"search_web",
            "description": "Search the internet for current , real time, or latest information. Use this when the question needs up to date data, recent events , scores , news , or anything that changes over time . Do not use for general Knowledge,maths or simple facts.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The Search query to look up"
                    }
                },
                "required": ["query"]            
           }
        }
    }
]

def search_web(query):
    print(f" Searching: {query}")
    results = tavily_client.search(query, max_results=2)  # we need atleast 3 search results from web 
    search_data = ""
    for result in results["results"]:
        search_data += f"Source: {result['url']}\n"
        search_data += f"Content: {result['content']}\n\n"
    return search_data



messages = [
    {"role":"system","content": """"You are a helpful assistant with web search ability.
     Only use the search_web tool when you need current, real time, or latest information.
     For general knowledge, math, or simple facts — answer directly without searching."""}     # this is where we give the ai its personality
]

print("======AI Agent with Tool use======")
print("Type 'quit' to exit\n")

while True:
    user_input = input("You: ").strip()

    if not user_input:
        continue
    if user_input.lower() == "quit":
        print("Bye!")
        break

    messages.append ({"role": "user", "content": user_input})

    #First AI call - whether it should use web search?
    response = groq_client.chat.completions.create(
        model="moonshotai/kimi-k2-instruct",
        messages=messages,
        tools=tools,
        tool_choice = "auto"
    )

    response_message = response.choices[0].message

    #Checks if AI want to use tool
    try:
        if response_message.tool_calls:
            print(" AI decided to Search....")

           #getting the tool call details
            tool_call = response_message.tool_calls[0]
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)

           #Execute the web search
            search_results = search_web(tool_args["query"])

           #Add AI decision + searcg results to history
            messages.append(response_message)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": "search_web",
                "content": search_results
            })

            # Second AI call - now Ai has search results, generates final answer
            final_response = groq_client.chat.completions.create(
                model="moonshotai/kimi-k2-instruct",
                messages=messages
            )

            reply = final_response.choices[0].message.content

        else:
            #AI answered from memory
            print(" AI answered from memory")
            reply = response_message.content   

    except Exception as e:
        print(f"Error: {e}")
        reply = "Something went Wrong , please try again."

    messages.append({"role": "assistant", "content": reply})
    print(f"\nAI: {reply}\n")