

class SettingsForm:
    __key__ = None
    __form__ = []
    __template__ = '/flasky_settings/forms/default.html'
    btn_title = 'Send'

    @classmethod
    def on_data(cls, data):
        return 'Success'

    @classmethod
    def get_form(cls):
        return cls.__form__

    @classmethod
    def loop_elements(cls):
        for element in cls.get_form():
            yield element

    @classmethod
    def get_template(cls):
        return cls.__template__

    @classmethod
    def get_key(cls):
        return cls.__key__ or cls.__name__