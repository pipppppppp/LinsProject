from .. import db

class Vehicles(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    workshop_id = db.Column(db.Integer, db.ForeignKey("workshops.id"))
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))

    plate_number = db.Column(db.String(20), nullable=False)
    vehicle_brand = db.Column(db.String(50), nullable=False)
    vehicle_type = db.Column(db.String(100), nullable=False)
    vehicle_year = db.Column(db.Integer)
    vehicle_color = db.Column(db.String(30))

    created_at = db.Column(db.BigInteger, nullable=False)
    updated_at = db.Column(db.BigInteger, nullable=False)
    deleted_at = db.Column(db.BigInteger)
    is_delete = db.Column(db.Integer, nullable=False, server_default='0')

    # Relationship
    workshops = db.relationship("Workshops", back_populates="vehicles")
    customers = db.relationship("Customers", back_populates="vehicles")
    payments = db.relationship("Payments", back_populates="vehicles")

    def __repr__(self):
        return '<Vehicles {}>'.format(self.plate_number)