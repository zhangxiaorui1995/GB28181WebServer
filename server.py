import socket
from flask import Flask
from models.base import db
from utils.import_helper import ImportHelper


def create_web_app() -> Flask:
    web_app = Flask(__name__)
    web_app.debug = True
    web_app = register_web_blueprint(app=web_app)
    web_app.extensions["db"] = db
    create_tables()
    return web_app


def create_socket_app() -> socket:
    socket_app_path = "apps.socket_apps.sip_protocol.SIPProtocol"
    return ImportHelper.load_class(socket_app_path)()


def register_web_blueprint(app: Flask, blueprint_group: str = "default") -> Flask:
    blueprint_map = {
        "default": [
            "apps.web_apps.index.index_blueprint",
            "apps.web_apps.device_manager.device_blueprint",
        ]
    }
    for blueprint in blueprint_map.get(blueprint_group):
        app.register_blueprint(ImportHelper.load_class(blueprint))
    return app


def create_tables():
    device_model = ImportHelper.load_class("models.GBDeviceModel")
    with db:
        device_model.create_table()
