from bardapi import Bard
import os 

#get the BERD api-key
file_path = os.getenv("BARD_API_TOKEN_FILE")
with open(file_path, 'r') as file:
    api_token = file.read()

bard = Bard(token = api_token.strip())
print(bard.get_answer("What is your name")['content'])
