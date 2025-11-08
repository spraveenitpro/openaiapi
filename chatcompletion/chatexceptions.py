import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)



client = OpenAI()

try:
    response_1 = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the capital of france?"},
        ],
        max_completion_tokens=3
    )
except openai.APIError as e:
    print(f"OpenAI API returned an API Error: {e}")
    pass
except openai.APIConnectionError as e:
    print(f"OpenAI API returned an API Error: {e}")
    pass
except openai.RateLimitError as e:
     #Handle rate limit error (we recommend using exponential backoff)
    print(f"OpenAI API request exceeded rate limit: {e}")
    pass




print (response_1.choices[0].message.content)