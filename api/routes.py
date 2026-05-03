from flask import Blueprint, jsonify, request

from api.services import search_player_by_name, search_players_by_club

api_bp = Blueprint("api", __name__)


@api_bp.route("/")
def home():
    return jsonify(
        {
            "message": "Player Analysis API",
            "examples": [
                "/api/player?name=Saka",
                "/api/club?club=Arsenal",
            ],
        }
    )


@api_bp.route("/api/player")
def get_player():
    name = request.args.get("name")

    if not name:
        return jsonify({"error": "Missing parameter: name"}), 400

    try:
        data = search_player_by_name(name)
        return jsonify({"total": len(data), "data": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/api/club")
def get_club():
    club = request.args.get("club")

    if not club:
        return jsonify({"error": "Missing parameter: club"}), 400

    try:
        data = search_players_by_club(club)
        return jsonify({"total": len(data), "data": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500