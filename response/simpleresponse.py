from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


client = OpenAI()

response = client.responses.create(
    model="gpt-4o-mini",
    input="What is the capital of France?"
)

print(response.output_text)

print(response.model_dump_json(indent=2))