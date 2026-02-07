from flask import request, jsonify, current_app
from functools import wraps
import jwt


def token_required(f):
    @wraps(f)
    def decorated(*args, **view_args):
        token = None
        if "Authorization" in request.headers:
            try:
                auth_header = request.headers.get("Authorization")
                token = auth_header.split(" ")[1]
                
            except IndexError:
                return jsonify({"message": "Token Malformado"}), 401
            
        if not token:
            return jsonify({"error": "Token não encontrado"}), 401
        
        try:
            data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token Expirado"}), 401
        
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token Inválido"}), 401
        
        return f(data, *args, **view_args)
    return decorated
