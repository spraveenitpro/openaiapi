# %% Setup
import os
from dotenv import load_dotenv
from openai import OpenAI, RateLimitError, APIConnectionError, APITimeoutError
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
    retry_if_exception_type,
)  # for exponential backoff
load_dotenv()


client = OpenAI()

@retry(
    wait=wait_random_exponential(min=1, max=60),
    stop=stop_after_attempt(6),
    retry=retry_if_exception_type((RateLimitError, APIConnectionError, APITimeoutError))
)
def response_with_backoff(client, **kwargs):
    return client.responses.create(**kwargs)

# %%  Basic text example  with search

response =response_with_backoff(
    client,
    model="gpt-4o-mini",
    tools=[{"type": "web_search"}],
    input="Did Elon Musk get his one trillion pay package?"
    
)

print(response.output_text)