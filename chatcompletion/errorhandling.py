import os
from openai import OpenAI, AuthenticationError, RateLimitError
from dotenv import load_dotenv

load_dotenv(override=True)


api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)



try:
    response_1 = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a summarizer who can summarize text into bullet points."},
        {"role": "user", "content": "Help me write a tweet for our new Hazelnut Mocha brew.?"},
    ],
    max_tokens=10)
except AuthenticationError as e:
    print(f" OpenAI API failed to authenticate {e}")
    pass
except RateLimitError as e:
    print(f" OpenAI API request exceeded rate limit {e}")
    pass
except Exception as e:
    print(f"Unable to generate a response, Exception: {e}")


# Response format


print (response_1.choices[0].message.content)