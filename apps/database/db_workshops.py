from .. import db

class Workshops(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    parent_id = db.Column(db.Integer, nullable=False, server_default='0', comment="0=Parent, others=Branch")
    workshop_name = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Integer, nullable=False, server_default='0')
    created_at = db.Column(db.BigInteger, nullable=False)
    updated_at = db.Column(db.BigInteger, nullable=False)
    deleted_at = db.Column(db.BigInteger, nullable=True)
    is_delete = db.Column(db.Integer, nullable=False, server_default='0')

    # Relationship
    users = db.relationship("Users", back_populates="workshops")
    categories = db.relationship("Categories", back_populates="workshops")
    products = db.relationship("Products", back_populates="workshops")
    customers = db.relationship("Customers", back_populates="workshops")
    payment = db.relationship("Payment", back_populates="workshops")
    
    def __repr__(self):
        return '<Workshops {}>'.format(self.workshop_name)