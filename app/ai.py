import os
from dotenv import load_dotenv
from openai import OpenAI

from app.workflows import actions

load_dotenv()

client = OpenAI(
    api_key = os.environ['OPENAI_API_KEY'],
    project = 'proj_bYSbdZ8axKmPKi6YWogxhpRx'
)

def pick_action(user_input: str) -> int:
    completion = client.chat.completions.create(
        model = 'gpt-4o',
        messages = [
            {'role': 'system', 'content': f"""
                Context: You are an AI assistant, with the role of selecting the required
                action from a list of actions, given user input in natural language.
                Output only the corresponding id, associated with the correct action.
                If the user input does not match any action, output 'Fail'.
                ActionList: {actions}
            """},
            {'role': 'user', 'content': f'UserInput: "{user_input}"'}
        ]
    )
    result = completion.choices[0].message.content
    if not result or result == 'Fail':
        print('Failed to pick action')
        exit(1)
    return int(result)

def speech_to_text(audio_file_path: str) -> str:
    audio_file = open(audio_file_path, 'rb')
    transcription = client.audio.transcriptions.create(
        model = 'whisper-1',
        file = audio_file,
        language = 'en'
    )
    return transcription.text

