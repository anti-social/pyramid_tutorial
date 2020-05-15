from wtforms import Form
from wtforms import SelectField
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms.validators import Length


class ProductForm(Form):
    name = StringField(validators=[DataRequired(), Length(max=100)])
    status = SelectField(choices=[(0, 'Active'), (1, 'Draft')], coerce=int)
