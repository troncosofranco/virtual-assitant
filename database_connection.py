import pymysql

config = {'host':'sql10.freemysqlhosting.net','user':'sql10513065','password':'B81hC65Arn','db':'sql10513065'}
#Object connection to the database
def get_connection():
    return pymysql.connect(**config)
        

def create_table():
    conn = get_connection()
    create_user_table = "CREATE TABLE usersData (name varchar(50), surname varchar(50), email varchar(50) );" 
    db_cursor = conn.cursor()
    db_cursor.execute(create_user_table)
    db_cursor.close()
    conn.close()
    

    

def delete_user(user):
    conn = get_connection()
    delete_user_query = "DELETE FROM usersData WHERE name = %s AND surname = %s AND email = %s;"
    db_cursor = conn.cursor()
    params = (user['name'], user['surname'], user['email'])
    db_cursor.execute(delete_user_query, params) # user Parameters )
    db_cursor.close()
    conn.commit()
    conn.close()

def insert_all_users(user_list):
    conn = get_connection()
    db_cursor = conn.cursor()
    insert_user_query = "INSERT INTO usersData (name, surname, email) VALUES (%s, %s, %s);"
    
    for user in user_list:
        params = (user['name'], user['surname'], user['email'])
        db_cursor.execute(insert_user_query, params) # user Parameters
    db_cursor.close()
    conn.commit()
    conn.close()

users = [
    {
        'name': 'John',
        'surname': 'Smith',
        'email': 'jhonsmith@gmail.com'
    },
    {
        'name': 'Jane',
        'surname': 'Maria',
        'email': 'jane@gmail.com'
    }
]


insert_all_users(users)