from app.api.db_manager.db_config import DatabaseConnection

with DatabaseConnection() as cursor:
    sql =  "CREATE TABLE IF NOT EXISTs users( user_id SERIAL PRIMARY KEY, username VARCHAR(100) NOT NULL, email VARCHAR(100) NOT NULL UNIQUE, password VARCHAR(12) NOT NULL)"
    sql1 = "CREATE TABLE IF NOT EXISTs replies(reply_id SERIAL PRIMARY KEY, qtn_id INT NOT NULL, user_id INT NOT NULL, reply_desc VARCHAR(100) NOT NULL)"
    sql2 = "CREATE TABLE IF NOT EXISTs questions(qtn_id SERIAL PRIMARY KEY, user_id INTEGER NOT NULL, title VARCHAR(100) NOT NULL UNIQUE, subject VARCHAR(200) NOT NULL, qtn_desc VARCHAR(100) NOT NULL)"
    cursor.execute(sql)
    cursor.execute(sql1)
    cursor.execute(sql2)