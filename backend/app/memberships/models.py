from app.extensions import db

class MembershipPlan(db.Model):
    __tablename__ = 'membership_plans'

    id = db.Column(db.Integer, primary_key=True)
    # Make club_id nullable for global plans
    club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'), nullable=True)
    name = db.Column(db.String(100), nullable=False)          # "Standard" or "Premium"
    price = db.Column(db.Float, nullable=False)               # one-time price
    duration_months = db.Column(db.Integer, nullable=False)   # 1, 3, 6, 12
    benefits = db.Column(db.Text)
    discount_percentage = db.Column(db.Float, default=0.0)    # 50 or 100
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

class Membership(db.Model):
    __tablename__ = 'memberships'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('membership_plans.id'), nullable=False)
    club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'), nullable=True)
    status = db.Column(db.String(20), default='active')
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    auto_renew = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    plan = db.relationship('MembershipPlan', lazy=True)