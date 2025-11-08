


from openai import OpenAI
from dotenv import load_dotenv

# Setup the OpenAI client
load_dotenv(override=True)


client = OpenAI()

completion_stream = client.chat.completions.create(
    model="gpt-4o-mini",
    temperature=0.7,
    messages=[
        {"role": "system", "content": "You are a summarizer of popular books and will provide a summary of the book in bullet points"},
        {"role": "user", "content": "please give a summary of the book How to Win Friends and Influence People by Dale Carnegie"},
    ],
    stream=True,
    max_tokens=100
)


for event in completion_stream:
    if event.choices:
        content = event.choices[0].delta.content
        if content:
            print(content, end="", flush=True)