from flask import Blueprint, Flask
from werkzeug.local import LocalProxy

blueprint: Blueprint
app: Flask
logger = LocalProxy(lambda: app.logger)
codec_string = 'utf-8'

def create_blueprint(flask_app, name: str = 'settings'):
    global app
    global blueprint
    global logger

    app = flask_app
    _set_defautl_configs(app)

    blueprint = Blueprint(
        name,
        __name__,
        template_folder="templates",
        static_folder="static"
    )
    blueprint.add_app_template_global(name, name='__flasky_settings_name__')

    from flasky_settings import main

    return blueprint

def _set_defautl_configs(app):
    app.config.setdefault('FLSETT_AUTO_SAVE_SETTINGS', False)

