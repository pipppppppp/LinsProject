from .. import db

class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    workshop_id = db.Column(db.Integer, db.ForeignKey("workshops.id"))
    customer_name = db.Column(db.String(100), nullable=False)
    customer_address = db.Column(db.Text)
    customer_phone = db.Column(db.String(15), nullable=False)
    created_at = db.Column(db.BigInteger, nullable=False)
    updated_at = db.Column(db.BigInteger, nullable=False)
    deleted_at = db.Column(db.BigInteger)
    is_delete = db.Column(db.Integer, nullable=False, server_default='0')

    # Relationship
    workshops = db.relationship("Workshops", back_populates="customers")
    payment = db.relationship("Payment", back_populates="customers")

    def __repr__(self):
        return '<Customers {}>'.format(self.customer_name)