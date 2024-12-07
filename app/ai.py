import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

from app.workflows import actions

load_dotenv()

client = OpenAI(
    api_key = os.environ['OPENAI_API_KEY'],
    project = 'proj_bYSbdZ8axKmPKi6YWogxhpRx'
)

class Action(BaseModel):
    id: int
    parameter: str

def pick_action(user_input: str):
    completion = client.beta.chat.completions.parse(
        model = 'gpt-4o',
        messages = [
            {'role': 'system', 'content': f"""
                Context: You are an AI assistant, with the role of selecting the required
                action from a list of actions, given user input in natural language.
                Output the corresponding <id>, associated with the correct action,
                along with an intuitive <parameter> for the function. For example, if the user
                says 'Modify the card number starting with 0123', the <parameter> will equal
                to '0123'.
                If the user input does not match any action, <id> is -1, and <parameter> is 'Fail'.
                ActionList: {actions}
            """},
            {'role': 'user', 'content': f'UserInput: "{user_input}"'}
        ],
        response_format = Action,
    )
    result = completion.choices[0].message.content
    if not result:
        print('Failed to pick action')
        exit(1)
    return json.loads(result)

def speech_to_text(audio_file_path: str) -> str:
    audio_file = open(audio_file_path, 'rb')
    transcription = client.audio.transcriptions.create(
        model = 'whisper-1',
        file = audio_file,
        language = 'en'
    )
    return transcription.text

