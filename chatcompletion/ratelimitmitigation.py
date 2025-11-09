from openai import OpenAI, RateLimitError, APIConnectionError, APITimeoutError
from dotenv import load_dotenv
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
    retry_if_exception_type,
)  # for exponential backoff
load_dotenv(override=True)

client = OpenAI()


@retry(
    wait=wait_random_exponential(min=1, max=60),
    stop=stop_after_attempt(6),
    retry=retry_if_exception_type((RateLimitError, APIConnectionError, APITimeoutError))
)
def response_with_backoff(client, **kwargs):
    return client.responses.create(**kwargs)


def ask_question(client, question):
    response = response_with_backoff(
        client,
        model="gpt-4o-mini",
        input=question
    )
    print(response)
    print(response.output_text)
    return response


def main():
    ask_question(client, "What is the capital of France?")


if __name__ == "__main__":
    main()