import tiktoken

encoding = tiktoken.encoding_for_model("gpt-4o-mini")
prompt = "Create a specialized AI assistant tailored for data science tasks"

num_tokens = len(encoding.encode(prompt))
print(num_tokens)