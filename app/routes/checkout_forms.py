from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, RadioField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, Regexp

class CheckoutForm(FlaskForm):
    order_type = RadioField(
        "Order Type",
        choices=[("delivery", "Delivery"), ("pickup", "Pickup (15% off)")],
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

    # Payment fields (DEMO UI — do NOT store card numbers)
    cardholder_name = StringField("Cardholder name", validators=[DataRequired(), Length(max=120)])
    card_number = StringField(
    "Card number",
    validators=[
        DataRequired(),
        Regexp(r"^\d{4} ?\d{4} ?\d{4} ?\d{4}$", message="Enter a valid 16-digit card number.")
    ],
)
    expiry = StringField(
        "Expiry (MM/YY)",
        validators=[DataRequired(), Regexp(r"^(0[1-9]|1[0-2])\/\d{2}$", message="Use MM/YY format.")]
    )
    cvc = StringField(
        "CVC",
        validators=[DataRequired(), Regexp(r"^\d{3,4}$", message="Enter a valid CVC.")]
    )

    submit = SubmitField("Place order")
