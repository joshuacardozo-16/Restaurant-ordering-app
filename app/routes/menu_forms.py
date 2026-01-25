from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class MenuItemForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=120)])
    description = TextAreaField("Description", validators=[Optional(), Length(max=1000)])
    price = DecimalField("Price (£)", validators=[DataRequired(), NumberRange(min=0)], places=2)
    category = StringField("Category", validators=[DataRequired(), Length(max=50)])
    image_url = StringField("Image URL", validators=[Optional(), Length(max=500)])
    is_available = BooleanField("Available", default=True)
    submit = SubmitField("Save")
