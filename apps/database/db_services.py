from .. import db

class Services(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    workshop_id = db.Column(db.Integer, db.ForeignKey("workshops.id"))
    name = db.Column(db.String(150), nullable=False)
    service_fee = db.Column(db.BigInteger, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.BigInteger, nullable=False)
    updated_at = db.Column(db.BigInteger, nullable=False)
    deleted_at = db.Column(db.BigInteger)
    is_delete = db.Column(db.Integer, nullable=False, server_default="0")

    # Relationship
    workshops = db.relationship("Workshops", back_populates="services")
    sale_service_details = db.relationship("SaleServiceDetails", back_populates="services")

    def __repr__(self):
        return f"<Service {self.name}>"