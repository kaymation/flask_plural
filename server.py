from flask import Flask
from flask import render_template, url_for, g, request
import psycopg2

app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/new_question')
def new_question():
    sql_query = "SELECT * FROM questions ORDER BY RANDOM() LIMIT 1;"
    curr = get_db()
    curr.execute(sql_query)
    question_raw = curr.fetchone()
    question_id = question_raw[0]
    question = question_raw[1]
    answer_query = "SELECT body, correct FROM answers WHERE question_id = (%s);"
    curr.execute(answer_query, (question_id,))
    answers_raw = curr.fetchall()
    answers = map(lambda x: {"body": x[0], "correct": x[1]}, answers_raw)
    return render_template('single_question.json', question=question, answers=enumerate(answers), last=len(answers) - 1 )

@app.route('/index')
def index():
    return render_template('index.html')
    
def get_db():
    try:
        g.db_conn = psycopg2.connect("dbname='pluralsight'")
    except:
        print "I am unable to connect to the database"
    return g.db_conn.cursor()
