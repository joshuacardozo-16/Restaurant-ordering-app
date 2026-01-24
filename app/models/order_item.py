from ..extensions import db

class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)

    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False, index=True)
    order = db.relationship("Order", back_populates="items")

    menu_item_id = db.Column(db.Integer, db.ForeignKey("menu_items.id"), nullable=False, index=True)
    menu_item = db.relationship("MenuItem", back_populates="order_items")

    quantity = db.Column(db.Integer, nullable=False, default=1)

    unit_price_at_time = db.Column(db.Numeric(10, 2), nullable=False)
    line_total = db.Column(db.Numeric(10, 2), nullable=False)

    def set_totals(self):
        self.line_total = (self.unit_price_at_time or 0) * (self.quantity or 0)
