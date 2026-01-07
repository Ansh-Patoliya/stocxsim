from database.user_stock_dao import get_stock_tokens_by_user


def get_watchlist_tokens(user_id):
    return get_stock_tokens_by_user(user_id)
