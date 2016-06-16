A challenge for part of the Pluralsight application process, in three parts

1) A parser that populates a database from a CSV file
2) An API endpoint for presenting, listing, creating, and editing questions
3) A javascript front-end allowing users to answer questions, view a paginated listing, and sort questions

Innstructions to run locally:
This solution depends on flask and python, as well as postgresql
flask can be installed by following the instructions here: http://flask.pocoo.org/docs/0.11/installation/

once both are set up, run the following commands in order from the projects root directory:
$ createdb pluralsight
$ psql pluralsight < schema.sql
$ python seed.py
$ export FLASK_APP=server.py
$ flask run

