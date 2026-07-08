from .. import db

class Purchases(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.id"), nullable=False)
    workshop_id = db.Column(db.Integer, db.ForeignKey("workshops.id"), nullable=False)
    purchase_date = db.Column(db.BigInteger, nullable=False)
    total = db.Column(db.BigInteger, nullable=False, server_default="0")
    created_at = db.Column(db.BigInteger, nullable=False)
    updated_at = db.Column(db.BigInteger, nullable=False)
    deleted_at = db.Column(db.BigInteger)
    is_delete = db.Column(db.Integer, nullable=False, server_default="0")

    # Relationships
    suppliers = db.relationship("Suppliers", back_populates="purchases")
    workshops = db.relationship("Workshops", back_populates="purchases")
    purchase_details = db.relationship("PurchaseDetails", back_populates="purchases")

    def __repr__(self):
        return f"<Purchase {self.id}>"