import sqlite3
from sqlite3.dbapi2 import Cursor, connect

def create_connection():
    connection = sqlite3.connect("brain.db")
    return connection

def get_table():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM preguntas_y_respuestas")
    return cursor.fetchall()

bot_list = list()

def get_questions_answers():
    rows = get_table()
    for row in rows:
        print(row)
        bot_list.extend(list(row))
    return bot_list

#get_questions_answers()