from flask import Blueprint, render_template, session, request, jsonify
from service.order_service import get_order_details
from service.stockservice import get_stock_detail_service

orders_bp = Blueprint("orders_bp", __name__)


class DUser:
    def __init__(self, username=None, email=None, balance=0):
        self.username = username
        self.email = email
        self.balance = balance


@orders_bp.route("/order/history", methods=["POST"])
def order_history():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "User not logged in"}), 401
    
    filter_params = request.json.get("filter_params", {})

    try:
        orders = get_order_details(user_id, filter_params)
        return jsonify({
            "orders": orders
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400
