from datetime import datetime
from ..extensions import db

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    user = db.relationship("User", back_populates="orders")

    order_type = db.Column(db.String(20), nullable=False)  # delivery / pickup
    status = db.Column(db.String(30), nullable=False, default="pending")

    total_price = db.Column(db.Numeric(10, 2), nullable=False, default=0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Delivery fields (if order_type == 'delivery')
    delivery_address_line1 = db.Column(db.String(255), nullable=True)
    delivery_address_line2 = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(80), nullable=True)
    postcode = db.Column(db.String(20), nullable=True)
    delivery_instructions = db.Column(db.Text, nullable=True)

    # Pickup fields (if order_type == 'pickup')
    pickup_time_requested = db.Column(db.String(40), nullable=True)

    items = db.relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    def recalc_total(self):
        self.total_price = sum([item.line_total for item in self.items]) if self.items else 0
