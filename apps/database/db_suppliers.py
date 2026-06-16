from .. import db

class Suppliers(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama = db.Column(db.String(100), nullable=False)
    telepon = db.Column(db.String(20), nullable=False)
    alamat = db.Column(db.Text)
    created_at = db.Column(db.BigInteger, nullable=False)
    updated_at = db.Column(db.BigInteger, nullable=False)
    deleted_at = db.Column(db.BigInteger, nullable=True)
    is_delete = db.Column(db.Integer, nullable=False, server_default='0')
    
    def __repr__(self):
        return '<Suppliers {}>'.format(self.name)