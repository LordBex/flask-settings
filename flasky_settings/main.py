
from . import blueprint
from .settings import SettingClass
from .forms import SettingsForm
from flask import request, current_app
from .error import FormNotFound

@blueprint.get('/')
def ping():
    return 'ping'


@blueprint.post('/s/<setting_key>/set')
def set_value(setting_key):
    setting: SettingClass = SettingClass.get_group(setting_key)
    if not setting:
        return 'Failed'
    setting.set_properties(request.json)
    if current_app.config.get('FLSETT_AUTO_SAVE_SETTINGS'):
        setting.save()
    return 'Success'


@blueprint.post('/f/<form_key>')
def setting_form_enpoint(form_key):
    for subc in SettingsForm.__subclasses__():
        if subc.get_key() == form_key:
            r = subc.on_data(request.json)
            if r is True:
                return 'Success'
            if r is None:
                return 'Unknow State'
            return r
    raise FormNotFound(form=form_key)

