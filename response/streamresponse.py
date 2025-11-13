from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

response = client.responses.create(
    model="gpt-4o-mini",
    input="Tell me a bed time story in 3 lines",
    #tools=[{"type": "web_search"}],
    stream=True,
)

full_response = ""
for event in response:
    if event.type == "response.output_text.delta":
        print(event.delta, end="", flush=True)
        full_response += event.delta

print(f"\n\nFull response: {full_response}")