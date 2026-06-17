from .. import db

class SaleDetails(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    # Relasi ke tabel sales
    sale_id = db.Column(
        db.Integer,
        nullable=False
    )

    # Relasi ke tabel items
    item_id = db.Column(
        db.Integer,
        nullable=False
    )

    # Jumlah barang yang dijual
    qty = db.Column(
        db.Integer,
        nullable=False
    )

    # Harga jual saat transaksi
    harga_jual = db.Column(
        db.BigInteger,
        nullable=False
    )

    # Total per barang
    subtotal = db.Column(
        db.BigInteger,
        nullable=False
    )

    def __repr__(self):
        return '<SaleDetails {}>'.format(self.id)