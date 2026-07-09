from .. import db

class PurchaseDetails(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey("purchases.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_cost = db.Column(db.BigInteger, nullable=False)
    subtotal = db.Column(db.BigInteger, nullable=False)

    # Relationships
    purchases = db.relationship("Purchases", back_populates="purchase_details")
    products = db.relationship("Products", back_populates="purchase_details")

    def __repr__(self):
        return f"<PurchaseDetail {self.id}>"