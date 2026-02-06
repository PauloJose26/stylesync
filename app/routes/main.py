from flask import Blueprint, jsonify, request, current_app
from pydantic import ValidationError
from werkzeug.exceptions import UnsupportedMediaType
from bson import ObjectId
from datetime import datetime, timedelta, timezone
import jwt

from app.models.usuario_login import LoginPayload
from app.models.produto import *
from app.decorators import token_required
from app import db


main_bp = Blueprint("main_bp", __name__)


@main_bp.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Bem vindo ao StyleSync"})


@main_bp.route("/login", methods=["POST"])
def login():
    try:
        dados = request.get_json()
        dados_usuario = LoginPayload(**dados)

    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    except UnsupportedMediaType as e:
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


@main_bp.route("/produtos", methods=["GET"])
def listar_produtos():
    produtos_cursor = db.produtos.find({})
    lista_de_produtos = [
        ProdutoDBModel(**produto).model_dump(by_alias=True, exclude_none=True)
        for produto in produtos_cursor
    ]

    return jsonify(lista_de_produtos)


@main_bp.route("/produtos/<string:produto_id>", methods=["GET"])
def buscar_produto_por_id(produto_id):
    try:
        id_db = ObjectId(produto_id)

    except Exception as e:
        return jsonify(
            {"error": f"Erro ao transformar o {produto_id} em ObjectId: {e}"}
        )

    produto = db.produtos.find_one({"_id": id_db})
    if produto:
        return jsonify(
            ProdutoDBModel(**produto).model_dump(by_alias=True, exclude_none=True)
        )

    return jsonify({"erro": f"Produto com o id {produto_id} não encontrado"}), 404


@main_bp.route("/produtos", methods=["POST"])
@token_required
def cadastrar_produtos(token):
    try:
        dados = request.get_json()
        produto = ProdutoBase(**dados)
    except ValidationError as e:
        return jsonify({"error": e.errors()})

    resultado = db.produtos.insert_one(produto.model_dump())
    return (
        jsonify({"message": f"Produto criado", "id": str(resultado.inserted_id)}),
        201,
    )


@main_bp.route("/produtos/<int:produto_id>", methods=["PUT"])
def deletar_produto(produto_id):
    return jsonify(
        {"message": f"Esta é a rota de deleção do produto com o id {produto_id}"}
    )


@main_bp.route("/produtos/<int:produto_id>", methods=["DELETE"])
def atualizar_produto(produto_id):
    return jsonify(
        {"message": f"Esta é a rota de atualização do produto com o id {produto_id}"}
    )


@main_bp.route("/sales/upload", methods=["POST"])
def upload_produto():
    return jsonify({"message": "Esta é a rota de upload do arquivo de vendas"})
