from .. import db

class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    category_id = db.Column(db.Integer, nullable=False)

    nama_barang = db.Column(db.String(100), nullable=False)

    stok = db.Column(db.Integer,nullable=False, server_default='0')

    harga_beli = db.Column(db.Integer, nullable=False)

    harga_jual = db.Column(db.Integer,nullable=False)

    created_at = db.Column(db.BigInteger, nullable=False)
    updated_at = db.Column(db.BigInteger, nullable=False)

    deleted_at = db.Column(db.BigInteger)
    is_delete = db.Column(db.Integer, nullable=False, server_default='0')
    
    def __repr__(self):
        return '<Items {}>'.format(self.nama_barang)