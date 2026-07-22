from .. import db

class Payments(db.Model):
          
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))
    workshop_id = db.Column(db.Integer, db.ForeignKey("workshops.id"))
    cashier_id = db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicles.id"))
    invoice = db.Column(db.String(30), unique=True, nullable=True)
    payment_date = db.Column(db.BigInteger, nullable=False)
    total = db.Column(db.BigInteger, nullable=False)
    paid = db.Column(db.BigInteger, nullable=False,default=0)
    change = db.Column(db.BigInteger, nullable=False, default=0)
    created_at = db.Column(db.BigInteger, nullable=False)
    updated_at = db.Column(db.BigInteger, nullable=False)
    deleted_at = db.Column(db.BigInteger)
    is_delete = db.Column(db.Integer, nullable=False, server_default='0')

    # Relationship
    workshops = db.relationship("Workshops", back_populates="payments")
    customers = db.relationship("Customers", back_populates="payments")
    vehicles = db.relationship("Vehicles", back_populates="payments")
    sale_details = db.relationship("SaleDetails", back_populates="payments")
    sale_service_details = db.relationship("SaleServiceDetails", back_populates="payments")
    cashier = db.relationship("Users",foreign_keys=[cashier_id])
    # admin = db.relationship("Admins", primaryjoin="Sales.admin_id == Admins.id", foreign_keys=[admin_id], uselist=False)

    def __repr__(self):
        return '<Payment {}>'.format(self.id)