from flask import Blueprint

badges_bp = Blueprint('badges', __name__)

from . import logic
