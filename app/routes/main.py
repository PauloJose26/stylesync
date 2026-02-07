from flask import Blueprint, jsonify, request, current_app
from pydantic import ValidationError
from werkzeug.exceptions import UnsupportedMediaType
from datetime import datetime, timedelta, timezone
import jwt

from app.models.usuario_login import LoginPayload
from app.models.produto import *
from .produtos_blueprint import produtos_bp
from .usuarios_blueprint import usuarios_bp
from app import db


main_bp = Blueprint("main_bp", __name__)
main_bp.register_blueprint(produtos_bp)
main_bp.register_blueprint(usuarios_bp)


@main_bp.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Bem vindo ao StyleSync"})


@main_bp.route("/sales/upload", methods=["POST"])
def upload_produto():
    return jsonify({"message": "Esta é a rota de upload do arquivo de vendas"})
