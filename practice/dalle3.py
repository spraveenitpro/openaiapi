from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)

client = OpenAI()


print (client)

response = client.images.generate(
  model="dall-e-3",
  prompt="a cute teddy bear frolicking through a candy forest ",
  n=1,
  size="1024x1024"
)

print(response.model_dump_json(indent=2))