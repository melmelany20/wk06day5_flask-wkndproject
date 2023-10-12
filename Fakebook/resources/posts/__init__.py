from flask_smorest import Blueprint

bp = Blueprint('recipes', __name__, url_prefix='/recipe')

from . import routes