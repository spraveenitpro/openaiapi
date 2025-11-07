# for _ in range(100):
#     print ("hello")


num_stories = 10
content = "Once upon a time,"

prompt_lines = [f"Story #{i+1}: {content}" for i in range(num_stories)]
prompt_text = "\n".join(prompt_lines)


print (prompt_text)
