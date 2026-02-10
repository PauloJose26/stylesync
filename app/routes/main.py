from flask import Blueprint, jsonify, request, current_app
import csv
import os
import io
import pickle

from .produtos_blueprint import produtos_bp
from .usuarios_blueprint import usuarios_bp
from app.decorators import token_required
from app.models.oferta import Oferta
from app import db


main_bp = Blueprint("main_bp", __name__)
main_bp.register_blueprint(produtos_bp)
main_bp.register_blueprint(usuarios_bp)


@main_bp.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Bem vindo ao StyleSync"})


@main_bp.route("/sales/upload", methods=["POST"])
@token_required
def upload_produto(token):
    if "file" not in request.files:
        return jsonify({"error": "Nenhum arquivo foi enviado"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Nenhum arquivo selecionado"}), 400

    if file and file.filename.endswith(".csv"):
        csv_stream = io.StringIO(file.stream.read().decode("UTF-8"), newline=None)
        csv_reader = csv.DictReader(csv_stream)

        lista_de_ofertas = []
        erros_nos_registros = []

        for row_num, row in enumerate(csv_reader, 1):
            try:
                oferta_data = Oferta(**row)
                lista_de_ofertas.append(oferta_data.model_dump())

            except ValueError as e:
                erros_nos_registros.append(f"Linha {row_num} com dados inválidos")
            except Exception:
                erros_nos_registros.append(
                    f"Linha {row_num} com erro inesperado nos dados"
                )

        if lista_de_ofertas:
            try:
                print(lista_de_ofertas, end="\n\n")
                db.ofertas.insert_many(lista_de_ofertas)

            except Exception as e:
                return jsonify({"erro": e.args}), 400

        return jsonify(
            {
                "message": "Upload realizado com sucesso",
                "vendas_importadas": len(lista_de_ofertas),
                "erros_encontrados": erros_nos_registros,
            }
        )

    return jsonify({"message": "Esta é a rota de upload do arquivo de vendas"})
