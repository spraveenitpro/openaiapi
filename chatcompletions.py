import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)


def main():
    client = OpenAI()

    # Define price per token

    input_token_price = 0.15 / 1000000
    output_token_price = 0.6 / 1000000
    max_completion_tokens = 100

    # Read ticket.txt file
    with open("ticket.txt", "r", encoding="utf-8") as f:
        text = f.read() 
    
    response_1 = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a summarizer who can summarize text into bullet points."},
        {"role": "user", "content": f"Summarize this customer chat in 3 points {text}"},
    ],
    max_completion_tokens=max_completion_tokens
    )

    input_tokens =response_1.usage.prompt_tokens
    output_tokens = max_completion_tokens

    # Calculate cost
    cost = (input_tokens * input_token_price + output_token_price * max_completion_tokens)
    
    print (response_1.choices[0].message.content)
    print(f"Estimated cost: ${cost}")
    # Your code here


if __name__ == "__main__":
    main()