from flask import Flask
from flask import render_template, url_for, g, request, jsonify
import psycopg2
import json

app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/new_question')
def new_question():
    sql_query = "SELECT * FROM questions ORDER BY RANDOM() LIMIT 1;"
    curr = get_db().cursor()
    curr.execute(sql_query)
    question_raw = curr.fetchone()
    question_id = question_raw[0]
    question = question_raw[1]
    answer_query = "SELECT body, correct FROM answers WHERE question_id = (%s);"
    curr.execute(answer_query, (question_id,))
    answers_raw = curr.fetchall()
    answers = map(lambda x: {"body": x[0], "correct": x[1]}, answers_raw)
    return jsonify(question=question, answers=answers)
    # return render_template('single_question.json', question=question, answers=enumerate(answers), last=len(answers) - 1 )

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/list')
def list():
    order = "id" if request.values.get('sort') == "created" else "body"
    limit = 10
    offset = (int(request.values.get('page'))-1) * limit
    sql_string = "SELECT id, body FROM questions ORDER BY " + order + " LIMIT (%s) OFFSET (%s);"
    cur = get_db().cursor()
    cur.execute(sql_string, (limit, offset))
    questions_raw = cur.fetchall()
    result = map(lambda x: question_obj(x[0], x[1]), questions_raw)
    return jsonify(result)

@app.route('/new', methods=['POST'])
def create():
    question = request.values.get('question')
    answer = request.values.get('correct')
    distractors = request.values.getlist('distractors[]')
    conn = get_db()
    curr = conn.cursor()
    question_query = "INSERT INTO questions (body) VALUES (%s) RETURNING id;"
    answers_query = "INSERT INTO answers (body, correct, question_id) VALUES (%s, %s, %s)"
    curr.execute(question_query, (question,))
    question_id = curr.fetchone()[0]
    curr.execute(answers_query, (answer, True, question_id))
    if distractors is not None:
        for distractor in distractors:
            curr.execute(answers_query, (distractor, False, question_id))
    conn.commit()
    return jsonify(success=True)

@app.route('/update', methods=['POST'])
def update():
    data = json.loads(request.values.get('json'))
    question = data['question']
    answers = data['answers']
    checkAndUpdateQuestion(question)
    length = answers['length']
    for i in range(length):
        checkAndUpdateAnswer(answers[str(i)], question["id"])
    return jsonify(success=True)

def checkAndUpdateQuestion(question):
    conn = get_db()
    curr = conn.cursor()
    update_string = "UPDATE questions SET body = (%s) WHERE id = (%s);"
    curr.execute(update_string, (question["body"], question["id"]))
    conn.commit()
    return

def checkAndUpdateAnswer(answer, question_id):
    conn = get_db()
    curr = conn.cursor()
    if( 'id' in answer ):
        update_string = "UPDATE answers SET body = (%s) WHERE id = (%s);"
        curr.execute(update_string, (answer["body"], answer["id"]))
    else:
        new_answer_string = "INSERT INTO answers (body, correct, question_id) VALUES (%s, %s, %s);"
        params = (answer["body"], answer["correct"], question_id)
        curr.execute(new_answer_string, params)
    conn.commit()
    return

def question_obj(id, body):
    curr = get_db().cursor()
    sql_string = "SELECT id, body, correct FROM answers WHERE question_id = (%s) ORDER BY correct;"
    curr.execute(sql_string, (id,))
    answers_raw = curr.fetchall()
    result = {"id": id, "body": body, "answers": map(lambda x: {"id": x[0], "body": x[1]}, answers_raw)}
    return result

def get_db():
    try:
        g.db_conn = psycopg2.connect("dbname='pluralsight'")
    except:
        print "I am unable to connect to the database"
    return g.db_conn

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'db_conn'):
        g.db_conn.close()
