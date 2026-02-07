from flask import Blueprint

from app.models.usuario_login import *
from app.decorators import token_required
from app import db


usuarios_bp = Blueprint("usuarios_bp", __name__)


