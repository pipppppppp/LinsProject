from .. import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(20), nullable=False, server_default='1', comment="0=Administrator, 1=Owner, 2=Cashier")
    is_active = db.Column(db.Integer, nullable=False, server_default='0')
    created_at = db.Column(db.BigInteger, nullable=False)
    updated_at = db.Column(db.BigInteger, nullable=False)
    deleted_at = db.Column(db.BigInteger, nullable=True)
    is_delete = db.Column(db.Integer, nullable=False, server_default='0')

    # Relationship
    workshops = db.relationship("Workshops", back_populates="Users")
    
    def __repr__(self):
        return '<Users {}>'.format(self.username)