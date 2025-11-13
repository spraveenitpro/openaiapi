

## ✅ Challenge 1 — Summarizer Factory

# **Goal:** Build a function factory that returns a summarizer function using the Chat Completions API.

# ```python
# def create_summarizer(style: str):
#     """
#     Returns a function that summarizes text in a given style.
#     Example: 'bullet points', 'tweet', or 'executive summary'.
#     """
#     # TODO: Implement using OpenAI Chat Completions API
#     # The returned function should accept a text string
#     # and return a summary in the given style.
# ```

# **Hints**
# - Use `client.chat.completions.create()`  
# - Model: `"gpt-4o-mini"` or `"gpt-4-turbo"`  
# - Focus on modular structure: separate API call logic from prompt logic.


from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)

client = OpenAI()

def create_summarizer(style: str):
    """
    Returns a function that summarizes text in a given style.
    """

    def summarizer(text:str):
        prompt = f"Summarize the following text in {style} format: {text}"
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    return summarizer


# Test the summarizer
if __name__ == "__main__":
    tweet_summarizer = create_summarizer("tweet")
    print(tweet_summarizer("Hello, how are you?"))