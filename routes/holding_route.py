from flask import Blueprint, jsonify, session
# from service.holding_service import get_holdings_by_user
from database.holding_dao import get_holdings_by_user


holding_bp = Blueprint('holding_bp', __name__)


@holding_bp.route("/order", methods=["POST"])
def get_user_holdings():
    try:
        user_id = session.get("user_id")
        print("User ID in session:", user_id)

        if not user_id:
            return jsonify({"error": "User not logged in"}), 401

        holdings = get_holdings_by_user(user_id)

        return jsonify({
            "holdings": holdings
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 400
