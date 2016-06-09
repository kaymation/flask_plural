from flask import Flask
from flask import render_template, url_for
app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/new_question')
def new_question():
    return 'Something'
