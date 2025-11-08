import os
from openai import OpenAI
from dotenv import load_dotenv

from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential
)

load_dotenv(override=True)

client = OpenAI()
model="gpt-4o-mini"
messages=[
        {"role": "system", "content": "You are a helpful assistant who responds in json"},
        {"role": "user", "content": "What is the capital of france?"},
    ]


@retry(wait=wait_random_exponential(min=1,max=60),stop=stop_after_attempt(6) )
def get_response(model, message):

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        response_format={"type": "json_object"}
    )

    return (response.choices[0].message.content)


print(get_response(model, messages))