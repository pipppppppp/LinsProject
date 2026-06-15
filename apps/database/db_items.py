from .. import db

class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(75), nullable=False)

    category_id = db.Column(
        db.Integer,
        db.ForeignKey('categories.id')
    )

    harga_beli = db.Column(db.Integer)
    harga_jual = db.Column(db.Integer)

    stock = db.Column(db.Integer, default=0)

    created_at = db.Column(db.BigInteger, nullable=False)
    updated_at = db.Column(db.BigInteger, nullable=False)

    deleted_at = db.Column(db.BigInteger)
    is_delete = db.Column(db.Integer, nullable=False, server_default='0')
    
    def __repr__(self):
        return '<Categories {}>'.format(self.name)