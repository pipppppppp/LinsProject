from .. import db

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    workshop_id = db.Column(db.Integer, db.ForeignKey("workshops.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    product_name = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.Integer,nullable=False, server_default='0')
    purchase_price = db.Column(db.Integer, nullable=False)
    selling_price = db.Column(db.Integer,nullable=False)
    created_at = db.Column(db.BigInteger, nullable=False)
    updated_at = db.Column(db.BigInteger, nullable=False)
    deleted_at = db.Column(db.BigInteger)
    is_delete = db.Column(db.Integer, nullable=False, server_default='0')

    # Relationship
    workshops = db.relationship("Workshops", back_populates="products")
    categories = db.relationship("Categories", back_populates="products")
    sale_details = db.relationship("SaleDetails", back_populates="products")
    purchase_details = db.relationship("PurchaseDetails", back_populates="products")
    
    def __repr__(self):
        return '<Products {}>'.format(self.product_name)