# AI Agent with Web Search

I was genuinely surprised that you can build a working AI agent 
in under 100 lines of Python. No fancy frameworks. No complex setup.
Just API calls, a while loop, and one tricky JSON structure.

This is a terminal-based AI agent that searches the web in real time
and decides on its own when to search vs when to answer from memory.

## What it does

- Answers simple questions instantly from memory
- Searches the web automatically for anything current or recent
- Remembers the full conversation across messages
- Tells you whether it searched or used memory

## The part that clicked everything

Tool use. You describe a function to the AI in plain English using JSON,
and the AI figures out on its own when to call it. That's it.
That's how Perplexity works. That's how ChatGPT browses the web.

Getting that JSON structure right was honestly the hardest part of this 
project — one wrong key and the whole thing breaks silently.
When it finally ran and I saw "AI decided to search" for the first time,
that was a genuine sense of achievement.

## Stack

- Groq API — llama-3.3-70b-versatile
- Tavily — real time web search built for AI
- Python 3.12

## Run it yourself

git clone https://github.com/mishra-codes/AI-Agent.git
cd chatbot
python -m venv .venv
.venv\Scripts\activate
pip install groq tavily-python python-dotenv

Create a .env file:
GROQ_API_KEY=your_key
TAVILY_API_KEY=your_key

python chatbot.py

## Built by

Ayush Mishra — 2nd year CS student building toward AI engineering
github.com/mishra-codes
