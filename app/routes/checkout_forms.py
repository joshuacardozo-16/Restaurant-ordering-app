from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, RadioField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, Regexp

class CheckoutForm(FlaskForm):
    order_type = RadioField(
        "Order Type",
        choices=[("delivery", "Delivery"), ("pickup", "Pickup (15% off)")],
        default="delivery",
        validators=[Optional()],
    )

    # Delivery fields
    delivery_address_line1 = StringField("Address line 1", validators=[Optional(), Length(max=255)])
    delivery_address_line2 = StringField("Address line 2", validators=[Optional(), Length(max=255)])
    city = StringField("City", validators=[Optional(), Length(max=80)])
    postcode = StringField("Postcode", validators=[Optional(), Length(max=20)])
    delivery_instructions = TextAreaField("Delivery instructions", validators=[Optional(), Length(max=1000)])

    # Pickup fields
    pickup_time_requested = StringField("Pickup time (e.g. 18:30)", validators=[Optional(), Length(max=40)])

    # ✅ Payment fields become OPTIONAL (we enforce them only when total > 0 in the route)
    cardholder_name = StringField("Cardholder name", validators=[Optional(), Length(max=120)])

    card_number = StringField(
        "Card number",
        validators=[
            Optional(),
            Regexp(r"^\d{4} ?\d{4} ?\d{4} ?\d{4}$", message="Enter a valid 16-digit card number."),
        ],
    )

    expiry = StringField(
        "Expiry (MM/YY)",
        validators=[
            Optional(),
            Regexp(r"^(0[1-9]|1[0-2])\/\d{2}$", message="Use MM/YY format."),
        ],
    )

    cvc = StringField(
        "CVC",
        validators=[
            Optional(),
            Regexp(r"^\d{3,4}$", message="Enter a valid CVC."),
        ],
    )

    submit = SubmitField("Place order")


    # ✅ Enforce card details ONLY when server says payment is required
    def validate(self, extra_validators=None):
        ok = super().validate(extra_validators=extra_validators)
        if not ok:
            return False

        requires_payment = bool(getattr(self, "requires_payment", True))

        if requires_payment:
            # Enforce "required" on payment fields
            if not (self.cardholder_name.data or "").strip():
                self.cardholder_name.errors.append("Cardholder name is required.")
                return False

            if not (self.card_number.data or "").strip():
                self.card_number.errors.append("Card number is required.")
                return False

            if not (self.expiry.data or "").strip():
                self.expiry.errors.append("Expiry is required.")
                return False

            if not (self.cvc.data or "").strip():
                self.cvc.errors.append("CVC is required.")
                return False

        return True
