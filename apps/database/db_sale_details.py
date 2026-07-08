from .. import db

class SaleDetails(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    payment_id = db.Column(db.Integer, db.ForeignKey("payments.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.BigInteger, nullable=False)
    subtotal = db.Column(db.BigInteger, nullable=False)

    # Relationships
    payments = db.relationship("Payments", back_populates="sale_details")
    products = db.relationship("Products", back_populates="sale_details")

    def __repr__(self):
        return f"<SaleDetail {self.id}>"