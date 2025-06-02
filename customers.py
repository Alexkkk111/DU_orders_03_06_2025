from app import db

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    orders = db.relationship('Order', back_populates='customer')

    def dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }



