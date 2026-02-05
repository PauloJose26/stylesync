from flask import Flask
from pymongo import MongoClient

db = None


def create_app():
    global db
    app = Flask(__name__)
    app.config.from_object("config.Config")

    try:
        client = MongoClient(app.config["MONGO_URI"])
        db = client.get_default_database()

    except Exception as e:
        print(f"Erro ao realizar a conexão com o banco de dados {e}")

    from app.routes.main import main_bp
    app.register_blueprint(main_bp)

    return app
