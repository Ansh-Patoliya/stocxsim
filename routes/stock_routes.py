from data.live_data import LIVE_PRICES, BASELINE_DATA
from flask import Blueprint, request, jsonify, render_template, session
from database.user_stock_dao import get_stock_tokens_by_user
from service.stockservice import search_stocks_service, get_stock_detail_service

stock_bp = Blueprint("stock_bp", __name__)


@stock_bp.route("/search")
def search_stocks():
    query = request.args.get("q", "").strip()

    if not query:
        return jsonify([])

    return jsonify(search_stocks_service(query))


@stock_bp.route("/<stock_token>")
def stock_detail(stock_token):
    stock = get_stock_detail_service(stock_token)

    if not stock:
        return render_template("404.html"), 404

    return render_template("stock.html", stock=stock)


@stock_bp.route("/watchlist-page")
def watchlist_page():
    return render_template("watchlist.html")


@stock_bp.route("/watchlist")
def api_watchlist():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify([])   # or return 401

    tokens = get_stock_tokens_by_user(user_id)

    result = []

    for token in tokens:
        token = int(token)
        ltp = LIVE_PRICES.get(token, None)
        base = BASELINE_DATA.get(token, None)

        change = 0
        change_pct = 0

        if ltp and base:
            change = round(ltp - base, 2)
            change_pct = round((change / base) * 100, 2)

        result.append({
            "token": token,
            "price": ltp,
            "change": change,
            "change_pct": change_pct
        })

    return jsonify(result)
