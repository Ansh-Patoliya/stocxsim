from database.connection import get_connection

def insert_order(order_details):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO orders (user_id, symbol_token, quantity, order_type, price, transaction_type)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor.execute(query, (
        order_details["user_id"],
        order_details["symbol_token"],
        order_details["quantity"],
        order_details["order_type"],
        order_details["price"],
        order_details["transaction_type"]
    ))

    conn.commit()
    cursor.close()
    conn.close()