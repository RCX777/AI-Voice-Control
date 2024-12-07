from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/hello/<name>', methods=['GET'])
def hello(name: str):
    return f'Hello, {name}!', 200

