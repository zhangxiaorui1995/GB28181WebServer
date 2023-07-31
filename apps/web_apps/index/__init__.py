from flask import Blueprint

index_blueprint = Blueprint("index", __name__)

from .controller import *
from .views import *
