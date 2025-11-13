# ## ✅ Challenge 3 — Tone Rewriter Factory

# **Goal:** Return a function that rewrites text into a specific tone.

# ```python
# def tone_rewriter(tone: str):
#     """
#     Returns a function that rewrites text into the desired tone.
#     Example tones: 'formal', 'friendly', 'supportive', 'concise'.
#     """
#     # TODO: Implement using the Chat Completions API
# ```

# **Focus:** Show modularity — one function builds a “prompt template,” another executes the API call.

# ---
"""Tone Rewriter Factory - Modular implementation with proper documentation."""

from typing import Callable
from openai import OpenAI
from openai.types.chat import ChatCompletionMessage
from dotenv import load_dotenv

# Configuration constants
DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_TEMPERATURE = 0.5

# Initialize OpenAI client
load_dotenv()
_client = OpenAI()


def build_system_prompt(tone: str) -> str:
    """
    Build a system prompt for the specified tone.
    
    Args:
        tone: The desired writing tone (e.g., 'formal', 'friendly', 'supportive').
    
    Returns:
        A formatted system prompt string.
    
    Example:
        >>> build_system_prompt("formal")
        "You are a writer who writes in formal tone"
    """
    return f"You are a writer who writes in {tone} tone"


def build_user_prompt(text: str) -> str:
    """
    Build a user prompt for text rewriting.
    
    Args:
        text: The text to be rewritten.
    
    Returns:
        A formatted user prompt string.
    
    Example:
        >>> build_user_prompt("Hello")
        "rewrite this text Hello"
    """
    return f"rewrite this text {text}"


def rewrite_text(
    client: OpenAI,
    tone: str,
    text: str,
    model: str = DEFAULT_MODEL,
    temperature: float = DEFAULT_TEMPERATURE,
) -> str:
    """
    Rewrite text in a specific tone using the OpenAI Chat Completions API.
    
    Args:
        client: An initialized OpenAI client instance.
        tone: The desired writing tone.
        text: The text to be rewritten.
        model: The OpenAI model to use. Defaults to 'gpt-4o-mini'.
        temperature: Sampling temperature (0.0 to 2.0). Defaults to 0.5.
    
    Returns:
        The rewritten text as a string.
    
    Raises:
        ValueError: If the input text is empty or None.
        Exception: If the API call fails.
    
    Example:
        >>> client = OpenAI()
        >>> rewrite_text(client, "formal", "Hello, how are you?")
        "Greetings, how are you faring today?"
    """
    if not text or not text.strip():
        raise ValueError("Input text cannot be empty")
    
    system_prompt = build_system_prompt(tone)
    user_prompt = build_user_prompt(text)
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=temperature,
    )
    
    message: ChatCompletionMessage = response.choices[0].message
    if not message.content:
        raise ValueError("Received empty response from API")
    
    return message.content.strip()


def tone_rewriter(tone: str, client: OpenAI | None = None) -> Callable[[str], str]:
    """
    Factory function that returns a tone-specific text rewriter function.
    
    This function creates a closure that captures the tone and OpenAI client,
    returning a callable that rewrites text in the specified tone.
    
    Args:
        tone: The desired writing tone (e.g., 'formal', 'friendly', 'supportive').
        client: Optional OpenAI client instance. If None, uses the module-level client.
    
    Returns:
        A function that takes text as input and returns rewritten text in the specified tone.
    
    Example:
        >>> formal_writer = tone_rewriter("formal")
        >>> formal_writer("Hello, how are you?")
        "Greetings, how are you faring today?"
        
        >>> friendly_writer = tone_rewriter("friendly")
        >>> friendly_writer("Hello, how are you?")
        "Hey there! How's it going?"
    """
    if client is None:
        client = _client
    
    def writer(text: str) -> str:
        """
        Rewrite text in the captured tone.
        
        Args:
            text: The text to be rewritten.
        
        Returns:
            The rewritten text in the specified tone.
        """
        return rewrite_text(client, tone, text)
    
    return writer


def main() -> None:
    """Example usage of the tone rewriter factory."""
    # Create tone-specific writers
    formal_writer = tone_rewriter("formal")
    friendly_writer = tone_rewriter("friendly")
    supportive_writer = tone_rewriter("supportive")
    pirate_writer = tone_rewriter("pirate")
    
    # Test text to rewrite
    test_text = "Hello, how are you?"
    
    # Demonstrate different tones
    print(f"Original: {test_text}\n")
    print(f"Formal: {formal_writer(test_text)}")
    print(f"Friendly: {friendly_writer(test_text)}")
    print(f"Supportive: {supportive_writer(test_text)}")
    print(f"Pirate: {pirate_writer(test_text)}")


if __name__ == "__main__":
    main()

    
    