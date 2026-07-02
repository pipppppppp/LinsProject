from .. import db

class PurchaseDetails(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    purchase_id = db.Column(db.Integer, nullable=False)
    item_id = db.Column(
        db.Integer,
        nullable=False
    )
    qty = db.Column(
        db.Integer,
        nullable=False
    )
    harga_beli = db.Column(
        db.Integer,
        nullable=False
    )
    subtotal = db.Column(
        db.Integer,
        nullable=False
    )
    def __repr__(self):
        return '<PurchaseDetails {}>'.format(self.id)