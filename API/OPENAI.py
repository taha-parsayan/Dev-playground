import openai
from openai.error import RateLimitError

openai.api_key = open("openai-api-key.txt", "r").read().strip('\n')

completion = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    messages = [
        {"role": "user", "content":"Who are you?"}
    ]
)

print(completion)
