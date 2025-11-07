from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()



def ask_question(client, file, question):
    response = client.responses.create(
        model="gpt-4o",
        input=[
            {
                "role": "user",
                "content": [{
                    "type": "input_file",
                    "file_id": file.id
                }, {
                    "type": "input_text",
                    "text": question
                }]
            }
        ]
    )
    return (response.output_text)




def main():
    client = OpenAI()

    file = client.files.create(
        file=open("test.pdf","rb"),
        purpose="user_data"
    )

    while True:
        question = input("Enter a question: ")
        if question.lower() == "exit":
            break
        print(ask_question(client, file, question))




if __name__ == "__main__":
    main()
