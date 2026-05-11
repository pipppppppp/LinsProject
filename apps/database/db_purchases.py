from .. import db

class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    created_at = db.Column(db.BigInteger, nullable=False)
    updated_at = db.Column(db.BigInteger, nullable=False)
    deleted_at = db.Column(db.BigInteger, nullable=True)
    is_delete = db.Column(db.Integer, nullable=False, server_default='0')
    
    def __repr__(self):
        return '<Categories {}>'.format(self.name)