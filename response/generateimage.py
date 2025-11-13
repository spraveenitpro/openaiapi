from dotenv import load_dotenv
from openai import OpenAI, PermissionDeniedError

load_dotenv(override=True)

client = OpenAI()

response = client.responses.create(
    model="o4-mini",
    input="generate an image of a beautiful sunset over a calm ocean",
)

# Save the image to a file
image_data = [
    output.result
    for output in response.output
    if output.type == "image_generation_call"
]

if image_data:
    image_base64 = image_data[0]
    with open("cat_and_otter.png", "wb") as f:
        f.write(base64.b64decode(image_base64))