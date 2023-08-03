import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv('api-key')
 
messages = [ {"role": "system", "content":
			"You are a intelligent assistant."} ]
def send_question(user_input):
	message = user_input
	if message:
		messages.append(
			{"role": "user", "content": message},
		)
		chat = openai.ChatCompletion.create(
			model="gpt-3.5-turbo", messages=messages
		)
	reply = chat.choices[0].message.content
	print(f"ChatGPT: {reply}")
	messages.append({"role": "assistant", "content": reply})
	return reply
	

