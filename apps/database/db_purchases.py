from .. import db

class Purchases(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    supplier_id = db.Column(
        db.Integer,
        nullable=False
    )

    admin_id = db.Column(
        db.Integer,
        nullable=False
    )

    admin = db.relationship(
        "Admins",
        primaryjoin="Purchases.admin_id == Admins.id",
        foreign_keys=[admin_id],
        uselist=False
    )

    tanggal = db.Column(
        db.BigInteger,
        nullable=False
    )

    total = db.Column(
        db.Integer,
        nullable=False,
        server_default='0'
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
        return '<Purchases {}>'.format(self.id)