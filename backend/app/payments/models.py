from app.extensions import db

class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='INR')
    payment_type = db.Column(db.String(30), nullable=False) # booking, membership, event
    reference_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='pending')
    gateway_transaction_id = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
