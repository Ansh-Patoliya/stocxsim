from flask import Blueprint, request, jsonify, render_template, session
from database.watchlist_dao import get_stock_tokens_by_user
from websockets.angle_ws import subscribe, unsubscribe, ws
from service.stockservice import search_stocks_service, get_stock_detail_service, rsi_cal, ema_cal, get_closes
from data.live_data import register_equity_token, LIVE_STOCKS
from websockets.angle_ws import subscribe, ws

stock_bp = Blueprint("stock_bp", __name__)


# for subscribing and unsubscribing stocks for live data (Specially for search)
@stock_bp.route("/subscribe/<token>", methods=["POST"])
def subscribe_stock(token):
    try:
        if ws is None:
            return jsonify({"error": "WS not connected"}), 500

        print("📡 SUBSCRIBE REQUEST:", token)

        subscribe(ws, 1, str(token))

        return jsonify({"status": "subscribed", "token": token})

    except Exception as e:
        print("❌ SUBSCRIBE ERROR:", e)
        return jsonify({"error": str(e)}), 500


@stock_bp.route("/unsubscribe/<token>", methods=["POST"])
def unsubscribe_stock(token):
    try:
        if ws is None:
            return jsonify({"error": "WS not connected"}), 500

        print("📡 UNSUBSCRIBE REQUEST:", token)

        unsubscribe(ws, 1, str(token))

        return jsonify({"status": "unsubscribed", "token": token})

    except Exception as e:
        print("❌ UNSUBSCRIBE ERROR:", e)
        return jsonify({"error": str(e)}), 500


# routes for stock details and search
@stock_bp.route("/search")
def search_stocks():
    query = request.args.get("q", "").strip()

    if not query:
        return jsonify([])

    return jsonify(search_stocks_service(query))


# Searched stock action route.
@stock_bp.route("/<stock_token>")
def stock_detail(stock_token):
    stock = get_stock_detail_service(stock_token)
    if not stock:
        return render_template("404.html"), 404

    # REGISTER TOKEN FOR LIVE UPDATES
    register_equity_token(str(stock_token))
    closes = get_closes(stock_token)
    stock.set_rsi(rsi_cal(closes))
    stock.set_ema_9(ema_cal(closes, 9))
    stock.set_ema_20(ema_cal(closes, 20))

    # Fetch user watchlist tokens
    user_id = session.get("user_id")
    watchlist_tokens = [str(t) for t in get_stock_tokens_by_user(
        user_id)] if user_id else []

    return render_template("stock.html", stock=stock, watchlist_tokens=watchlist_tokens)



