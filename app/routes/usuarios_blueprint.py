from flask import Blueprint, jsonify, request, current_app
from pydantic import ValidationError
from werkzeug.exceptions import UnsupportedMediaType
from datetime import datetime, timedelta, timezone
from bson import ObjectId
import hashlib
import jwt

from app.models.usuario_login import *
from app.decorators import token_required
from app import db


usuarios_bp = Blueprint("usuarios_bp", __name__)


@usuarios_bp.route("/usuarios", methods=["GET"])
def listar_usuarios():
    cursor_usuarios = db.usuarios.find({}, {"senha": 0})
    lista_de_usuarios = [
        UsuarioDBModel(**usuario).model_dump(by_alias=True, exclude_none=True)
        for usuario in cursor_usuarios
    ]

    return jsonify(lista_de_usuarios)


@usuarios_bp.route("/dashboard", methods=["GET"])
@token_required
def usuario_dashboard(token):
    usuario_id = token["user_id"]
    usuario = db.usuarios.find_one({"_id": ObjectId(usuario_id)}, {"senha": 0})

    if not usuario:
        return jsonify({"erro": "Usuário não encontrado. Token inválido"}), 404
    return jsonify(
        UsuarioDBModel(**usuario).model_dump(by_alias=True, exclude_none=True)
    )


@usuarios_bp.route("/usuarios", methods=["POST"])
def cadastrar_usuario():
    try:
        dados = request.get_json()
        usuario = UsuarioBase(**dados)
        
    except ValidationError as error:
        return jsonify({"error": error.errors()[0]["msg"]}), 400

    usuario_model_dump = usuario.model_dump()
    password_bytes = usuario_model_dump["senha"].encode("utf-8")
    hash_object = hashlib.sha256(password_bytes)
    usuario_model_dump["senha"] = hash_object.hexdigest()

    resultado = db.usuarios.insert_one(usuario_model_dump)

    return (
        jsonify({"message": f"Usuário cadastrado", "id": str(resultado.inserted_id)}),
        201,
    )


@usuarios_bp.route("/login", methods=["POST"])
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
    
    password_bytes = dados_usuario.password.encode("utf-8")
    hash_object = hashlib.sha256(password_bytes)
    usuario_db = db.usuarios.find_one(
        {"username": dados_usuario.username, "senha": hash_object.hexdigest()}
    )
    
    if not usuario_db:
        return jsonify({"error": "Credenciais inválidas"}), 403
    
    token = jwt.encode(
        {
            "user_id": str(usuario_db["_id"]),
            "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
        },
        current_app.config["SECRET_KEY"],
        algorithm="HS256",
    )
    return jsonify({"access_token": token}), 200
