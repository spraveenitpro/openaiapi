import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)


def main():
    client = OpenAI()

    # Read ticket.txt file
    with open("ticket.txt", "r", encoding="utf-8") as f:
        text = f.read() 
    
    response_1 = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a summarizer who can summarize text into bullet points."},
        {"role": "user", "content": "Help me write a tweet for our new Hazelnut Mocha brew.?"},
    ],
    )
    
    print (response_1.choices[0].message.content)
    # Your code here


if __name__ == "__main__":
    main()