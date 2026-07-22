from .. import db

class Cashiers(db.Model):
      id = db.Column(db.Integer, primary_key=True, autoincrement=True)
      user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
      workshop_id = db.Column(db.Integer, db.ForeignKey("workshops.id"), nullable=False)
      is_active = db.Column(db.Integer, nullable=False, server_default='1')
      created_at = db.Column(db.BigInteger, nullable=False)
      updated_at = db.Column(db.BigInteger, nullable=False)
      deleted_at = db.Column(db.BigInteger, nullable=True)
      is_delete = db.Column(db.String(3), nullable=False, server_default='0')

      # Relationship
      users = db.relationship("Users", back_populates="cashiers")
      workshops = db.relationship("Workshops", back_populates="cashiers")

      def __repr__(self):
            return '<Cashiers {}>'.format(self.id)