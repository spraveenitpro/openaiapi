import tiktoken

encoding = tiktoken.encoding_for_model("gpt-4o-mini")
prompt = "Create a specialized AI assistant tailored for data science tasks"

num_tokens = len(encoding.encode(prompt))
print(num_tokens)


# Method 1: Model-based (recommended)
encoding1 = tiktoken.encoding_for_model("gpt-4o-mini")
# Automatically uses "o200k_base" encoding

# Method 2: Direct encoding (fallback)
encoding2 = tiktoken.get_encoding("cl100k_base")
# Directly uses "cl100k_base" encoding

# These will give DIFFERENT token counts for the same text!
text = "Hello world"
print(len(encoding1.encode(text)))  # Might be 2 tokens
print(len(encoding2.encode(text)))  # Might be 2 tokens (or different!)