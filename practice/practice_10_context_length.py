"""
Scenario
--------
Customer: "I keep hitting context_length_exceeded on this giant prompt."
Focus: Explaining context windows, counting tokens, and strategies (chunking,
        summarizing, pagination) for oversized inputs.
Debug Path: Confirm model limits, suggest pre-processing, and teach the customer
            how to inspect usage tokens in the response.
"""

from openai import OpenAI, BadRequestError, RateLimitError
from dotenv import load_dotenv
load_dotenv()
import tiktoken
client = OpenAI()


def reproduce_issue(count: int) -> None:
    """Creates a prompt that's intentionally longer than the context window."""
    prompt = "word " * count  # Intentional bug: far beyond gpt-4-turbo capacity.
    messages = [{"role": "user", "content": prompt}]
    
    # Check token count before making API call
    fits, token_count, max_input = check_context_limit(messages, model="gpt-4-turbo")
    
    print(f"Token count: {token_count:,}")
    print(f"Max input tokens: {max_input:,}")
    print(f"Fits within limit: {fits}")
    
    if not fits:
        print(f"⚠️ Prompt exceeds limit by {token_count - max_input:,} tokens")
    
    try:
        client.chat.completions.create(
            model="gpt-4-turbo",
            messages=messages,
        )
    except BadRequestError as exc:
        print("Caught BadRequestError:", exc)
        print("Coach Tip: chunk/summarize inputs or leverage responses.stream().")

    except RateLimitError as exc:
        print("Caught RateLimitError:", exc)
        print("Coach Tip: Implement exponential backoff.")


def check_context_limit(messages: list[dict], model: str = "gpt-4-turbo") -> tuple[bool, int, int]:
    """
    Check if messages fit within model's context window.
    
    Args:
        messages: List of message dicts
        model: The OpenAI model name
    
    Returns:
        Tuple of (fits_within_limit, token_count, max_input_tokens)
    """
    # Model context limits (approximate)
    context_limits = {
        "gpt-4-turbo": 128_000,
        "gpt-4o": 128_000,
        "gpt-4o-mini": 128_000,
        "gpt-3.5-turbo": 16_385,
        "o1-preview": 200_000,
    }
    
    max_context = context_limits.get(model, 128_000)
    token_count = count_messages_tokens(messages, model)
    
    # Reserve ~4k tokens for response
    max_input_tokens = max_context - 4_000
    
    fits = token_count <= max_input_tokens
    return fits, token_count, max_input_tokens

def count_messages_tokens(messages: list[dict], model: str = "gpt-4-turbo") -> int:
    """
    Count total tokens in a messages array (as used in chat.completions.create).
    
    Args:
        messages: List of message dicts with 'role' and 'content' keys
        model: The OpenAI model name
    
    Returns:
        Total number of tokens including formatting overhead
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    
    # Formatting overhead: ~4 tokens per message
    tokens_per_message = 4
    
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(str(value)))
            if key == "name":  # If name field exists, add 1 token
                num_tokens += 1
    
    # Add 2 tokens for assistant reply priming
    num_tokens += 2
    
    return num_tokens


def estimate_tokens(text: str, model: str = "gpt-4-turbo") -> int:
    """
    Count tokens in text using tiktoken for the specified model.
    
    Args:
        text: The text to count tokens for
        model: The OpenAI model name (determines which encoding to use)
    
    Returns:
        Number of tokens in the text
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    except KeyError:
        # Fallback to cl100k_base encoding (used by gpt-4, gpt-3.5-turbo)
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))

if __name__ == "__main__":
    prompt = "word " * 28_000  # Intentional bug: far beyond gpt-4-turbo capacity.
    reproduce_issue(20_000)