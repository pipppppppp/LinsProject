from .. import db

class Services(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    nama_jasa = db.Column(
        db.String(150),
        nullable=False
    )

    biaya_jasa = db.Column(
        db.BigInteger,
        nullable=False
    )

    keterangan = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.BigInteger,
        nullable=False
    )

    updated_at = db.Column(
        db.BigInteger,
        nullable=False
    )

    deleted_at = db.Column(
        db.BigInteger
    )

    is_delete = db.Column(
        db.Integer,
        nullable=False,
        server_default='0'
    )

    def __repr__(self):
        return '<Services {}>'.format(
            self.nama_jasa
        )