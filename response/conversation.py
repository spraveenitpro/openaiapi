from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

client = OpenAI()

input_messages = [
    {
        "role": "user",
        "content": "Hello, how are you?"
    }
]

def chat_loop():
    current_response_id = None
    while True:
        # Get user input
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Goodbye!")
            break
        response = client.responses.create(
            model="gpt-4o-mini",
            input= user_input,
            previous_response_id = current_response_id
        )
        current_response_id = response.id
        # print response
        print("Assistant: ", response.output_text)


        

if __name__ == "__main__":
    chat_loop()






print(response.output_text)