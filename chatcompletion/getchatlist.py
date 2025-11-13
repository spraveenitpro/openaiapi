from openai import OpenAI, AuthenticationError, APIError, RateLimitError
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

try:
    response = client.chat.completions.list()
    print(response.model_dump_json(indent=2))
    first_id = response.data[0].id
    print( first_id)
except AuthenticationError as e:
    print(f"Authentication Error: {e}")
except APIError as e:
    print(f"API Error: {e}")
except RateLimitError as e:
    print(f"Rate Limit Error: {e}")
except Exception as e:
    print(f"Unexpected Error: {e}")


# Get chat messages
try:
    first_completion = client.chat.completions.retrieve(completion_id=first_id)
    messages = client.chat.completions.messages.list(completion_id=first_id)
    #print(first_chat.model_dump_json(indent=2))
    print(messages)
except AuthenticationError as e:
    print(f"Authentication Error: {e}")
except APIError as e:
    print(f"API Error: {e}")
except RateLimitError as e:
    print(f"Rate Limit Error: {e}")
except Exception as e:
    print(f"Unexpected Error: {e}")