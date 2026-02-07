from flask import Blueprint, jsonify, request, current_app
from pydantic import ValidationError
from werkzeug.exceptions import UnsupportedMediaType
from datetime import datetime, timedelta, timezone
import jwt

from app.models.usuario_login import LoginPayload
from app.models.produto import *
from .produtos_blueprint import produtos_bp
from app import db


main_bp = Blueprint("main_bp", __name__)
main_bp.register_blueprint(produtos_bp)


@main_bp.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Bem vindo ao StyleSync"})


@main_bp.route("/login", methods=["POST"])
def login():
    try:
        dados = request.get_json()
        dados_usuario = LoginPayload(**dados)

    except ValidationError as error:
        return jsonify({"error": error.errors()}), 400
    except UnsupportedMediaType as error:
        return (
            jsonify(
                {
                    "error": "Corpo da requisição inválido ou não é um JSON",
                }
            ),
            400,
        )

    if dados_usuario.username == "admin" and dados_usuario.password == "supersecret":
        token = jwt.encode(
            {
                "user_id": dados_usuario.username,
                "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
            },
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        )
        return jsonify({"access_token": token}), 200

    return jsonify({"error": "Credenciais inválidas"}), 401


@main_bp.route("/sales/upload", methods=["POST"])
def upload_produto():
    return jsonify({"message": "Esta é a rota de upload do arquivo de vendas"})
