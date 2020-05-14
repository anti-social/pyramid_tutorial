from wtforms import Form
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms.validators import Length


class ProductForm(Form):
    name = StringField(validators=[DataRequired(), Length(max=10)])
