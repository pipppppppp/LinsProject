from .. import db

class CashDeposits(db.Model):
    __tablename__ = "cash_deposits"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    workshop_id = db.Column(db.Integer, db.ForeignKey("workshops.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    deposit_date = db.Column(db.BigInteger, nullable=False)
    total_sales = db.Column(db.BigInteger, nullable=False, server_default="0")
    total_deposit = db.Column(db.BigInteger, nullable=False, server_default="0")
    difference = db.Column(db.BigInteger, nullable=False, server_default="0")
    notes = db.Column(db.Text)
    status = db.Column(db.Integer, nullable=False, server_default="0")
    verified_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    verified_at = db.Column(db.BigInteger)
    created_at = db.Column(db.BigInteger, nullable=False)
    updated_at = db.Column(db.BigInteger, nullable=False)
    deleted_at = db.Column(db.BigInteger)
    is_deleted = db.Column(db.Integer, nullable=False, server_default="0")

    # Relationships
    workshops = db.relationship("Workshops", back_populates="cash_deposits")
    users = db.relationship("Users", foreign_keys=[user_id], back_populates="cash_deposits")
    verifier = db.relationship("Users", foreign_keys=[verified_by], back_populates="verified_cash_deposits")

    def __repr__(self):
        return f"<CashDeposit {self.id}>"