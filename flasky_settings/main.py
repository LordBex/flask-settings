
from . import blueprint
from .settings import SettingClass
from .forms import SettingsForm
from flask import request, current_app
from .error import FormNotFound

@blueprint.get('/')
def ping():
    return 'ping'


@blueprint.post('/s/<setting_key>/set')               # TODO adding Event Function subscribe
def set_value(setting_key):
    setting: SettingClass = SettingClass.get_group(setting_key)
    if not setting:
        return 'Failed'
    setting.set_properties(request.json)
    if current_app.config.get('FLSETT_AUTO_SAVE_SETTINGS'):
        setting.save()
    return 'Success'


@blueprint.post('/f/<form_key>')               # TODO adding Event Function subscribe
def setting_form_enpoint(form_key):
    for subc in SettingsForm.__subclasses__():
        if subc.get_key() == form_key:
            subc.on_data(request.json)
            return 'Success'
    raise FormNotFound(form=form_key)

