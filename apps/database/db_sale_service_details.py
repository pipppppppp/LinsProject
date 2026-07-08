from .. import db

class SaleServiceDetails(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    payment_id = db.Column(db.Integer, db.ForeignKey("payments.id"), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey("services.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    service_price = db.Column(db.BigInteger, nullable=False)
    subtotal = db.Column(db.BigInteger, nullable=False)

    # Relationships
    payments = db.relationship("Payments", back_populates="sale_service_details")
    services = db.relationship("Services", back_populates="sale_service_details")

    def __repr__(self):
        return f"<SaleServiceDetail {self.id}>"