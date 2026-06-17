from .. import db

class Sales(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    customer_id = db.Column(
        db.Integer,
        nullable=False
    )

    tanggal = db.Column(
        db.BigInteger,
        nullable=False
    )

    total = db.Column(
        db.BigInteger,
        nullable=False
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
        return '<Sales {}>'.format(self.id)