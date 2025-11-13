import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)


api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Read ticket.txt file
with open("ticket.txt", "r", encoding="utf-8") as f:
    text = f.read() 

response_1 = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Help me write a tweet for our new Hazelnut Mocha brew.?"},
    ],
    max_completion_tokens=50
)


# Response format

response_2 = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You provide answers in JSON format"},
        {"role": "user", "content": "Provide 5 trees with their scientific names in json"},
    ],
    max_tokens=100,
    response_format={"type": "json_object"}

)

print (response_1.choices[0].message.content)