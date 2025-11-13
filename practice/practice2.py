## ✅ Challenge 2 — Language Translator Factory

# **Goal:** Write a function that returns another function to translate text into a specified language.

# ```python
# def translator_factory(target_language: str):
#     """
#     Returns a function that translates text into the target_language.
#     Example: translator_factory("French")("Hello") → "Bonjour"
#     """
#     # TODO: Use Chat Completions API for translation
# ```

# **Bonus:** Handle simple error cases (empty input, unsupported language).

"""Language Translator Factory - Modular implementation with proper documentation."""

from typing import Callable
from openai import OpenAI
from openai.types.chat import ChatCompletionMessage
from openai import APIError, APIConnectionError, RateLimitError
from dotenv import load_dotenv

# Configuration constants
DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_TEMPERATURE = 0.1

# Initialize OpenAI client
load_dotenv()
_client = OpenAI()


def build_system_prompt(target_language: str) -> str:
    """
    Build a system prompt for translation to the target language.
    
    Args:
        target_language: The target language for translation (e.g., 'French', 'Spanish').
    
    Returns:
        A formatted system prompt string.
    
    Example:
        >>> build_system_prompt("French")
        "You are a translating assistant who will translate to French"
    """
    return f"You are a translating assistant who will translate to {target_language}"


def build_user_prompt(text: str) -> str:
    """
    Build a user prompt for text translation.
    
    Args:
        text: The text to be translated.
    
    Returns:
        A formatted user prompt string.
    
    Example:
        >>> build_user_prompt("Hello")
        "translate this text Hello"
    """
    return f"translate this text {text}"


def translate_text(
    client: OpenAI,
    target_language: str,
    text: str,
    model: str = DEFAULT_MODEL,
    temperature: float = DEFAULT_TEMPERATURE,
) -> str:
    """
    Translate text to a target language using the OpenAI Chat Completions API.
    
    Args:
        client: An initialized OpenAI client instance.
        target_language: The target language for translation.
        text: The text to be translated.
        model: The OpenAI model to use. Defaults to 'gpt-4o-mini'.
        temperature: Sampling temperature (0.0 to 2.0). Defaults to 0.1 for more
            deterministic translations.
    
    Returns:
        The translated text as a string.
    
    Raises:
        ValueError: If the input text is empty or None.
        APIError: If the OpenAI API returns an error.
        APIConnectionError: If there's a connection issue with the API.
        RateLimitError: If the API rate limit is exceeded.
        Exception: For other unexpected errors.
    
    Example:
        >>> client = OpenAI()
        >>> translate_text(client, "French", "Hello")
        "Bonjour"
    """
    if not text or not text.strip():
        raise ValueError("Input text cannot be empty")
    
    system_prompt = build_system_prompt(target_language)
    user_prompt = build_user_prompt(text)
    
    try:
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
    
    except (APIError, APIConnectionError, RateLimitError) as e:
        # Re-raise API-specific errors with context
        raise type(e)(f"Translation failed: {str(e)}") from e


def translator_factory(
    target_language: str,
    client: OpenAI | None = None,
) -> Callable[[str], str]:
    """
    Factory function that returns a language-specific translator function.
    
    This function creates a closure that captures the target language and OpenAI client,
    returning a callable that translates text to the specified language.
    
    Args:
        target_language: The target language for translation (e.g., 'French', 'Spanish').
        client: Optional OpenAI client instance. If None, uses the module-level client.
    
    Returns:
        A function that takes text as input and returns translated text in the target language.
    
    Example:
        >>> french_translator = translator_factory("French")
        >>> french_translator("Hello")
        "Bonjour"
        
        >>> spanish_translator = translator_factory("Spanish")
        >>> spanish_translator("How are you?")
        "¿Cómo estás?"
    """
    if client is None:
        client = _client
    
    def translator(text: str) -> str:
        """
        Translate text to the captured target language.
        
        Args:
            text: The text to be translated.
        
        Returns:
            The translated text in the target language.
        """
        return translate_text(client, target_language, text)
    
    return translator


def main() -> None:
    """Example usage of the translator factory."""
    # Create language-specific translators
    french_translator = translator_factory("French")
    spanish_translator = translator_factory("Spanish")
    
    # Test text to translate
    test_text = "How are you!"
    
    # Demonstrate translations
    print(f"Original: {test_text}\n")
    try:
        print(f"French: {french_translator(test_text)}")
        print(f"Spanish: {spanish_translator(test_text)}")
    except (ValueError, APIError, APIConnectionError, RateLimitError) as e:
        print(f"Translation error: {e}")


if __name__ == "__main__":
    main()
