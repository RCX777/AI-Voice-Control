from flask import Flask, request, render_template
from app.ai import pick_action, speech_to_text
from app.globals import cards


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

@app.route('/process-card', methods=['POST'])
def process_card():
    card_number = ''.join([
        request.form['card-number-0'],
        request.form['card-number-1'],
        request.form['card-number-2'],
        request.form['card-number-3']
    ])
    cards[card_number] = {
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

    return "Card details processed successfully!", 200

@app.route('/ai', methods=['GET'])
def ai():
    transcript = speech_to_text('DisableSubscription.mp3')
    print(transcript)
    action_id = pick_action(transcript)
    return str(action_id)

