from .. import db

class Suppliers(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    workshop_id = db.Column(db.Integer, db.ForeignKey("workshops.id"))

    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text)

    created_at = db.Column(db.BigInteger, nullable=False)
    updated_at = db.Column(db.BigInteger, nullable=False)
    deleted_at = db.Column(db.BigInteger, nullable=True)
    is_delete = db.Column(db.Integer, nullable=False, server_default="0")

    # Relationship
    workshops = db.relationship("Workshops", back_populates="suppliers")
    purchases = db.relationship("Purchases", back_populates="suppliers")
    def __repr__(self):
        return f"<Supplier {self.name}>"