import sqlite3

def create_connection():
    connection = sqlite3.connect('brain.db')
    return connection

def get_table():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM questions_answers')
    return cursor.fetchall()

bot_list = list()
def get_question_answers():
    rows = get_table()
    for row in rows:
        bot_list.extend(list(row))
        print(row)
        bot_list.extend(list(row))
    return bot_list
get_question_answers()