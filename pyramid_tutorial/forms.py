from wtforms import Form
from wtforms import StringField


class ProductForm(Form):
    name = StringField()
