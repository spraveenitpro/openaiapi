# 🧠 OpenAI Chat Completions API — Coding Practice Challenges

These exercises are designed to simulate the **AI Coding Interview** for the **Senior Support Engineer** role at OpenAI.  
Each problem focuses on writing **modular, idiomatic Python code** that **returns a function** and **uses the Chat Completions API**.

---

## 🧩 Setup Instructions

```bash
pip install openai python-dotenv
```

Create a `.env` file with your key:

```bash
OPENAI_API_KEY=your_api_key_here
```

Then in your Python file:

```python
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
```

---

## ✅ Challenge 1 — Summarizer Factory

**Goal:** Build a function factory that returns a summarizer function using the Chat Completions API.

```python
def create_summarizer(style: str):
    """
    Returns a function that summarizes text in a given style.
    Example: 'bullet points', 'tweet', or 'executive summary'.
    """
    # TODO: Implement using OpenAI Chat Completions API
    # The returned function should accept a text string
    # and return a summary in the given style.
```

**Hints**
- Use `client.chat.completions.create()`  
- Model: `"gpt-4o-mini"` or `"gpt-4-turbo"`  
- Focus on modular structure: separate API call logic from prompt logic.

---

## ✅ Challenge 2 — Language Translator Factory

**Goal:** Write a function that returns another function to translate text into a specified language.

```python
def translator_factory(target_language: str):
    """
    Returns a function that translates text into the target_language.
    Example: translator_factory("French")("Hello") → "Bonjour"
    """
    # TODO: Use Chat Completions API for translation
```

**Bonus:** Handle simple error cases (empty input, unsupported language).

---

## ✅ Challenge 3 — Tone Rewriter Factory

**Goal:** Return a function that rewrites text into a specific tone.

```python
def tone_rewriter(tone: str):
    """
    Returns a function that rewrites text into the desired tone.
    Example tones: 'formal', 'friendly', 'supportive', 'concise'.
    """
    # TODO: Implement using the Chat Completions API
```

**Focus:** Show modularity — one function builds a “prompt template,” another executes the API call.

---

## ✅ Challenge 4 — AI Code Reviewer

**Goal:** Create a higher-order function that accepts a code block and returns a review function for improvements.

```python
def create_code_reviewer():
    """
    Returns a function that takes Python code as input
    and returns a list of improvement suggestions.
    """
    # TODO: Use Chat Completions API
```

**Example Usage**
```python
reviewer = create_code_reviewer()
print(reviewer("def add(a,b):return a+b"))
```

**Expected Output**
```
["Add a docstring", "Use type hints", "Add spacing around operators"]
```

---

## ✅ Challenge 5 — Dynamic Prompt Router

**Goal:** Return a function that chooses a system prompt dynamically based on the input type.

```python
def dynamic_prompt_router():
    """
    Returns a function that accepts (input_text) and:
      - If it’s a question → answers it.
      - If it’s code → reviews it.
      - If it’s long prose → summarizes it.
    """
    # TODO: Use conditional logic and Chat Completions API
```

**Evaluation**
- Demonstrates multi-branch logic.
- Tests ability to “think aloud” and reason through input classification.

---

## 🧠 Reflection Checklist

- [ ] Is your code modular and readable?
- [ ] Are your prompts clear and parameterized?
- [ ] Did you handle exceptions gracefully?
- [ ] Did you log useful debug info (tokens, status, response)?
- [ ] Could your code scale to multiple API calls or use async?

---

**Pro Tip 💡**  
During the interview, talk through your reasoning:
> “I’ll break this into smaller helper functions so the main logic is clear.”  
> “Let’s inspect the response object before extracting content.”  
> “If this fails due to a rate limit, I’d add exponential backoff.”

Good luck! Preparation builds confidence. 🚀
