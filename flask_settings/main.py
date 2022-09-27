
from . import blueprint
from .settings import SettingClass
from flask import request


@blueprint.get('/')
def ping():
    return 'ping'


@blueprint.post('/<setting_key>/set')               # TODO adding Event Function subscribe
def set_value(setting_key):
    setting: SettingClass = SettingClass.get_group(setting_key)
    if not setting:
        return 'Failed'
    setting.set_properties(request.json)
    return 'Success'

