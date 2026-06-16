from .. import db

class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    nama = db.Column(db.String(100), nullable=False)
    alamat = db.Column(db.Text)
    telepon = db.Column(db.String(20), nullable=False)

    created_at = db.Column(db.BigInteger, nullable=False)
    updated_at = db.Column(db.BigInteger, nullable=False)

    deleted_at = db.Column(db.BigInteger)
    is_delete = db.Column(db.Integer, nullable=False, server_default='0')

    def __repr__(self):
        return '<Customers {}>'.format(self.nama)