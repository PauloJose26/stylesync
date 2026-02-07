from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from bson import ObjectId

from app.models.produto import *
from app.decorators import token_required
from app import db


produtos_bp = Blueprint("produtos_bp", __name__)


@produtos_bp.route("/produtos", methods=["GET"])
def listar_produtos():
    produtos_cursor = db.produtos.find({})
    lista_de_produtos = [
        ProdutoDBModel(**produto).model_dump(by_alias=True, exclude_none=True)
        for produto in produtos_cursor
    ]

    return jsonify(lista_de_produtos)


@produtos_bp.route("/produtos/<string:produto_id>", methods=["GET"])
def buscar_produto_por_id(produto_id):
    try:
        id_db = ObjectId(produto_id)

    except Exception as error:
        return jsonify(
            {"error": f"Erro ao transformar o {produto_id} em ObjectId ({error})"}
        )

    produto = db.produtos.find_one({"_id": id_db})
    if produto:
        return jsonify(
            ProdutoDBModel(**produto).model_dump(by_alias=True, exclude_none=True)
        )

    return jsonify({"erro": f"Produto com o id {produto_id} não encontrado"}), 404


@produtos_bp.route("/produtos", methods=["POST"])
@token_required
def cadastrar_produtos(token):
    try:
        dados = request.get_json()
        produto = ProdutoBase(**dados)
    except ValidationError as error:
        return jsonify({"error": error.errors()}), 200

    resultado = db.produtos.insert_one(produto.model_dump())
    return (
        jsonify({"message": f"Produto criado", "id": str(resultado.inserted_id)}),
        201,
    )


@produtos_bp.route("/produtos/<string:produto_id>", methods=["PUT"])
@token_required
def atualizar_produto(token, produto_id):
    try:
        object_produto_id = ObjectId(produto_id)
        update_data = UpdateProduto(**request.get_json())

    except ValidationError as error:
        return jsonify({"error": error.errors()}), 400

    update_resultado = db.produtos.update_one(
        {"_id": object_produto_id}, {"$set": update_data.model_dump(exclude_unset=True)}
    )

    if update_resultado.matched_count == 0:
        return jsonify({"error": "Produto não encontrado"}), 404

    update_produto = db.produtos.find_one({"_id": object_produto_id})
    return (
        jsonify(
            ProdutoDBModel(**update_produto).model_dump(
                by_alias=True, exclude_none=True
            )
        ),
        204,
    )


@produtos_bp.route("/produtos/<string:produto_id>", methods=["DELETE"])
@token_required
def deletar_produto(token, produto_id):
    try:
        object_produto_id = ObjectId(produto_id)

    except ValidationError as error:
        return jsonify({"error": error.errors()}), 400

    produto_deletado = db.produtos.delete_one({"_id": object_produto_id})
    if produto_deletado.deleted_count == 0:
        return jsonify({"error": "Produto não econtrado"}), 404

    return jsonify(), 204
