from .. import db

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))
    workshop_id = db.Column(db.Integer, db.ForeignKey("workshops.id"))
    payment_date = db.Column(db.BigInteger, nullable=False)
    total = db.Column(db.BigInteger, nullable=False)
    paid = db.Column(db.BigInteger, nullable=False,default=0)
    change = db.Column(db.BigInteger, nullable=False, default=0)
    created_at = db.Column(db.BigInteger, nullable=False)
    updated_at = db.Column(db.BigInteger, nullable=False)
    deleted_at = db.Column(db.BigInteger)
    is_delete = db.Column(db.Integer, nullable=False, server_default='0')

    # Relationship
    workshops = db.relationship("Workshops", back_populates="payment")
    customers = db.relationship("Customers", back_populates="payment")
    # admin = db.relationship("Admins", primaryjoin="Sales.admin_id == Admins.id", foreign_keys=[admin_id], uselist=False)

    def __repr__(self):
        return '<Payment {}>'.format(self.id)