from flask import Blueprint, Flask
from werkzeug.local import LocalProxy

blueprint: Blueprint
app: Flask
logger = LocalProxy(lambda: app.logger)


def create_blueprint(flask_app, name: str = 'settings'):
    global app
    global blueprint
    global logger

    app = flask_app

    blueprint = Blueprint(
        name,
        __name__,
        template_folder="templates",
        static_folder="static"
    )
    blueprint.add_app_template_global(name, name='__flask_settings_name__')

    from flask_settings import main

    return blueprint



