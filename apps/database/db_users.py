from .. import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    owner_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    email_verified_at = db.Column(db.BigInteger, nullable=True)
    verification_token = db.Column(db.String(255), unique=True, nullable=True)
    verification_token_expired_at = db.Column(db.BigInteger, nullable=True)
    password = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(3), nullable=False, server_default='1', comment="0=Administrator, 1=Owner, 2=Cashier")
    is_active = db.Column(db.Integer, nullable=False, server_default='0')
    created_at = db.Column(db.BigInteger, nullable=False)
    updated_at = db.Column(db.BigInteger, nullable=False)
    deleted_at = db.Column(db.BigInteger, nullable=True)
    is_delete = db.Column(db.String(3), nullable=False, server_default='0')

    # Relationship
    workshops = db.relationship("Workshops", back_populates="users")
    cashiers = db.relationship("Cashiers", back_populates="users")
    cash_deposits = db.relationship("CashDeposits", foreign_keys="CashDeposits.user_id", back_populates="users")
    verified_cash_deposits = db.relationship("CashDeposits", foreign_keys="CashDeposits.verified_by", back_populates="verifier")
    
    def __repr__(self):
        return '<Users {}>'.format(self.username)