from flask import Flask, jsonify, request, render_template
from app.ai import pick_action, speech_to_text
from app.globals import cards

from app.workflows import actions

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/cardInformation', methods=['GET'])
def cardInformation():
    return render_template('cardInformation.html')

@app.route('/display_cards', methods=['GET'])
def display_cards():
    if not cards:
        return render_template('cardInformation.html')
    return render_template('display_cards.html', cards=cards)

@app.route('/subscription/choosePayment', methods=['GET'])
def choosePayment():
    if not cards:
        return render_template('cardInformation.html')
    return render_template('choosePayment.html', cards=cards)

@app.route('/subscription', methods=['GET'])
def subscription():
    return render_template('subscription.html')

@app.route('/process-card', methods=['POST'])
def process_card():
    card_number = ''.join([
        request.form['card-number-0'],
        request.form['card-number-1'],
        request.form['card-number-2'],
        request.form['card-number-3']
    ])
    cards[card_number] = {
        'id': card_number,
        'card_holder': request.form['card-holder'],
        'expiration_month': request.form['card-expiration-month'],
        'expiration_year': request.form['card-expiration-year'],
        'ccv': request.form['card-ccv'],
    }
    card_holder = request.form['card-holder']
    expiration_month = request.form['card-expiration-month']
    expiration_year = request.form['card-expiration-year']
    ccv = request.form['card-ccv']

    # Validare suplimentară pe server
    if len(card_number) != 16 or not card_number.isdigit():
        return "Invalid card number", 400
    if not card_holder:
        return "Card holder name is required", 400
    if not expiration_month or not expiration_year:
        return "Expiration date is required", 400
    if len(ccv) != 3 or not ccv.isdigit():
        return "Invalid CCV", 400
    print(cards)

    return render_template('display_cards.html', cards=cards)

@app.route('/post_audio', methods=['POST'])
def post_audio():
    audio_data = request.files['audio'].read()
    audio_file = open('/app/temp.mp3', 'wb')
    audio_file.write(audio_data)
    transcript = speech_to_text('/app/temp.mp3')
    print(transcript)
    action = pick_action(transcript)
    return actions[action['id']]['func'](action['parameter'])

@app.route('/ai', methods=['GET'])
def ai():
    transcript = speech_to_text('/app/audio-samples/RemoveCard.mp3')
    # transcript = 'Hello, I want to remove a credit card from the website. The credit card ID starts with 12345678'
    action = pick_action(transcript)
    return jsonify(actions[action['id']]['func'](action['parameter']))

@app.route('/cards', methods=['GET'])
def get_cards():
    return jsonify(cards)

