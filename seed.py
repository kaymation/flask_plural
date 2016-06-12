import psycopg2

try:
    conn = psycopg2.connect("dbname='pluralsight'")
except:
    print "I am unable to connect to the database"

cur = conn.cursor()

with open('code_challenge_question_dump.csv') as file:
    next(file)
    for line in file:
        parts = line.split("|")
        cur.execute("INSERT INTO questions (body) VALUES (%s) RETURNING id;", (parts[0],))
        question_id = cur.fetchone()[0]
        query_for_answer = "INSERT INTO answers (body, correct, question_id) VALUES (%s, %s, %s)";
        cur.execute(query_for_answer, (parts[1], True, question_id))
        distractors = parts[2].split(", ")
        for dist in distractors:
            cur.execute(query_for_answer, (dist.strip(), False, question_id))
conn.commit()
conn.close()
