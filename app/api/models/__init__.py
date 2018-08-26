from app.api.db_manager.db_config import DatabaseConnection

def check_table(sql, value):
    with DatabaseConnection as cursor:
        cursor.excecute(sql, value)
        return cursor.fetchone()

def check_users(user_id):
    return check_table("SELECT user_id FROM users WHERE user_id = %", [user_id]) 

def check_questions(qtn_id):
    return check_table("SELECT qtn_id FROM questions WHERE qtn_id = %", [qtn_id])
