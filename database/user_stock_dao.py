from database.connection import get_connection as gc

def get_stock_tokens_by_user(user_id):
    conn = gc()
    cursor = conn.cursor()
    query = "SELECT stock_token FROM user_stocks WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [row[0] for row in rows]
    