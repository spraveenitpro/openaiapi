from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv(override=True)


client = OpenAI()
model="gpt-4o-mini"
messages=[
        {"role": "system", "content": "You are a helpful assistant who responds in json"},
        {"role": "user", "content": "What is the capital of france?"},
    ]

response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant!"},
        {"role": "user", "content": "What is the capital of france?"}
    ],
    max_tokens=50  # too low
)

print(response.choices[0].message.content)