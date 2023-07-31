from flask import Blueprint

device_blueprint = Blueprint(
    "device_manager", __name__, url_prefix="/device", template_folder="./templates"
)

from .controller import *
from .views import *
