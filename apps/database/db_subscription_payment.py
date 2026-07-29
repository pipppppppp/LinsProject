from .. import db


class SubscriptionPayments(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    workshop_id = db.Column(db.Integer, db.ForeignKey("workshops.id"), nullable=False)
    order_id = db.Column(db.String(100), nullable=False, unique=True)
    amount = db.Column(db.Numeric(15, 2), nullable=False)
    transaction_id = db.Column(db.String(100), nullable=True)
    payment_type = db.Column(db.String(50), nullable=True)
    transaction_status = db.Column(db.String(30), nullable=False, server_default="pending")
    snap_token = db.Column(db.Text, nullable=True)
    paid_at = db.Column(db.BigInteger, nullable=True)
    created_at = db.Column(db.BigInteger, nullable=False)
    updated_at = db.Column(db.BigInteger, nullable=False)
    deleted_at = db.Column(db.BigInteger, nullable=True)
    is_delete = db.Column(db.Integer, nullable=False, server_default="0")

    # Relationship
    workshops = db.relationship("Workshops", back_populates="subscription_payments")

    def __repr__(self):
        return "<SubscriptionPayments {}>".format(self.order_id)