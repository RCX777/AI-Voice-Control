from flask import Flask, render_template
from app.ai import pick_action, speech_to_text


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/cardInformation', methods=['GET'])
def cardInformation():
    return render_template('cardInformation.html')

@app.route('/subscription', methods=['GET'])
def subscription():
    return render_template('subscription.html')

@app.route('/ai', methods=['GET'])
def ai():
    transcript = speech_to_text('DisableSubscription.mp3')
    print(transcript)
    action_id = pick_action(transcript)
    return str(action_id)

