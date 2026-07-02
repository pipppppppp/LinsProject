from .. import db

class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    workshop_id = db.Column(db.Integer, db.ForeignKey("workshops.id"))
    category = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.BigInteger, nullable=False)
    updated_at = db.Column(db.BigInteger, nullable=False)
    deleted_at = db.Column(db.BigInteger, nullable=True)
    is_delete = db.Column(db.Integer, nullable=False, server_default='0')
    
    # Relationship
    workshops = db.relationship("Workshops", back_populates="categories")
    products = db.relationship("Products", back_populates="categories")

    def __repr__(self):
        return '<Categories {}>'.format(self.category)