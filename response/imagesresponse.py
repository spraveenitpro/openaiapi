from openai import OpenAI
from dotenv import load_dotenv
import base64

load_dotenv(override=True)

client = OpenAI()

def encode_image(image_path):
    with open(image_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


image_path = "response/image.png"
base64_image = encode_image(image_path)

input_messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "input_text",
                "text": "Please describe these images in detail"           
            },
            {
                "type": "input_image",
                "image_url": f"data:image/jpeg;base64,{base64_image}"
            },
            {
                "type": "input_image",
                "image_url": "https://i.imgur.com/l2iRpbb.jpeg"
            },
        ]
    }
]
response = client.responses.create(
    model="gpt-4o-mini",
    input= input_messages,
)

print(response.output_text)