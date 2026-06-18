from .. import db

class SaleServiceDetails(db.Model):

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

    # Relasi ke tabel services
    service_id = db.Column(
        db.Integer,
        nullable=False
    )

    # Jumlah jasa
    qty = db.Column(
        db.Integer,
        nullable=False,
        default=1
    )

    # Harga jasa saat transaksi
    harga_jasa = db.Column(
        db.BigInteger,
        nullable=False
    )

    # Total jasa
    subtotal = db.Column(
        db.BigInteger,
        nullable=False
    )

    def __repr__(self):
        return '<SaleServiceDetails {}>'.format(
            self.id
        )