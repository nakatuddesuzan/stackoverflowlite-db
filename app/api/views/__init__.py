from app.api.db_manager.db_config import DatabaseConnection

def check_user(user_id):
    return check_table("SELECT id FROM users WHERE id = %s", [user_id])

def check_table(sql, value):
    with DatabaseConnection() as cursor:
        cursor.execute(sql,value)
        return cursor.fetchone()