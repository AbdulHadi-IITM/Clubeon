from datetime import date
from dateutil.relativedelta import relativedelta
from app.extensions import db
from app.memberships.models import MembershipPlan, Membership
from app.clubs.models import Club

class MembershipService:
    @staticmethod
    def get_plans(club_id=None):
        query = MembershipPlan.query.filter_by(is_active=True)
        if club_id:
            query = query.filter_by(club_id=club_id)
        return query.all()

    @staticmethod
    def subscribe(user_id, plan_id, auto_renew):
        plan = MembershipPlan.query.get(plan_id)
        if not plan or not plan.is_active:
            return None, {"code": "NOT_FOUND", "message": "Plan not found or inactive"}

        # Check if user already has an active membership for this club
        existing = Membership.query.filter_by(
            user_id=user_id,
            club_id=plan.club_id,
            status='active'
        ).first()

        if existing:
            return None, {"code": "CONFLICT", "message": "User already has an active membership for this club"}

        start_date = date.today()
        end_date = start_date + relativedelta(months=1)

        membership = Membership(
            user_id=user_id,
            plan_id=plan_id,
            club_id=plan.club_id,
            status='active',
            start_date=start_date,
            end_date=end_date,
            auto_renew=auto_renew
        )
        
        db.session.add(membership)
        db.session.commit()
        return membership, None

    @staticmethod
    def get_my_memberships(user_id):
        return Membership.query.filter_by(user_id=user_id).order_by(Membership.created_at.desc()).all()

    @staticmethod
    def cancel_membership(user_id, membership_id):
        membership = Membership.query.get(membership_id)
        if not membership:
            return False, {"code": "NOT_FOUND", "message": "Membership not found"}
            
        if membership.user_id != user_id:
            return False, {"code": "FORBIDDEN", "message": "Not authorized to cancel this membership"}
            
        if membership.status == 'cancelled':
            return False, {"code": "VALIDATION_ERROR", "message": "Membership is already cancelled"}

        membership.status = 'cancelled'
        membership.auto_renew = False
        db.session.commit()
        return True, None
