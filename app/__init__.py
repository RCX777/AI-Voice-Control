from flask import Flask, render_template
from app.ai import pick_action, speech_to_text


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/ai', methods=['GET'])
def ai():
    transcript = speech_to_text('DisableSubscription.mp3')
    print(transcript)
    action_id = pick_action(transcript)
    return str(action_id)

