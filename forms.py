from wtforms import Form
from wtforms.fields import StringField, PasswordField


class munForm (Form):
    municipio = StringField('municipio')