from .. import db
""" 
    # EXAMPLE
    |   id    |   username    |       email         |    Password   |     Role     |   is_active   |   created_at  |   updated_at  |   is_delete   |  deteleted_at  |
    |  (int)  |    (sting)    |      (string)       |    (strng)    |     (int)    |     (int)     |    (bigint)   |    (bigint)   |     (int)     |    (bigint)    |
    |---------|---------------|---------------------|---------------|--------------|---------------|---------------|---------------|---------------|----------------|
    |    1    |John Doe       |johndoe@gmail.com    |@JohnDoe1234   |       1      |       1       |1234567890     |1234567890     |       1       |1234567890      |
    |         |               |                     |               |              |               |               |               |               |                |  
"""

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(3), nullable=False, server_default='1', comment="0=Administrator, 1=Owner, 2=Cashier")
    is_active = db.Column(db.Integer, nullable=False, server_default='1')
    created_at = db.Column(db.BigInteger, nullable=False)
    updated_at = db.Column(db.BigInteger, nullable=False)
    deleted_at = db.Column(db.BigInteger, nullable=True)
    is_delete = db.Column(db.String(3), nullable=False, server_default='0')

    # Relationship
    workshops = db.relationship("Workshops", back_populates="users")
    cash_deposits = db.relationship("CashDeposits", foreign_keys="CashDeposits.user_id", back_populates="users")
    verified_cash_deposits = db.relationship("CashDeposits", foreign_keys="CashDeposits.verified_by", back_populates="verifier")
    
    def __repr__(self):
        return '<Users {}>'.format(self.username)