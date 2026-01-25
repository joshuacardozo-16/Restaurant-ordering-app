from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, RadioField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class CheckoutForm(FlaskForm):
    order_type = RadioField(
        "Order Type",
        choices=[("delivery", "Delivery"), ("pickup", "Pickup")],
        default="delivery",
        validators=[DataRequired()],
    )

    # Delivery fields
    delivery_address_line1 = StringField("Address line 1", validators=[Optional(), Length(max=255)])
    delivery_address_line2 = StringField("Address line 2", validators=[Optional(), Length(max=255)])
    city = StringField("City", validators=[Optional(), Length(max=80)])
    postcode = StringField("Postcode", validators=[Optional(), Length(max=20)])
    delivery_instructions = TextAreaField("Delivery instructions", validators=[Optional(), Length(max=1000)])

    # Pickup fields
    pickup_time_requested = StringField("Pickup time (e.g. 18:30)", validators=[Optional(), Length(max=40)])

    submit = SubmitField("Place order")
