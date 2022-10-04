class FormNotFound(Exception):
    def __init__(self, form, **data):
        self.message = f"Form '{str(form)}' is not a SubClass from SettingsForm !"
        self.append_data = data
        super().__init__(self.message)

    def __str__(self):
        return f'[FlaskSettings] {self.message}'

class ValidationError(Exception):
    def __init__(self, message=None, **data):
        self.message = message or "Error on Validation"
        self.append_data = data
        super().__init__(self.message)

    def __str__(self):
        return f'[FlaskSettings] {self.message}'


class ParsingError(Exception):
    def __init__(self, message=None, **data):
        self.message = message or "Error on Parsing"
        self.append_data = data
        super().__init__(self.message)

    def __str__(self):
        return f'[FlaskSettings] {self.message}'


class PropertyPermissionError(Exception):
    def __init__(self, message=None, property_name=None, **data):
        self.message = message or f"PermissionError on Property ({property_name})"
        self.append_data = data
        super().__init__(self.message)

    def __str__(self):
        return f'[FlaskSettings] {self.message}'