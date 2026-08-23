from datetime import date, timedelta
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
        else:
            # Global plans (club_id IS NULL)
            query = query.filter_by(club_id=None)
        return query.order_by(MembershipPlan.name, MembershipPlan.duration_months).all()

    @staticmethod
    def subscribe(user_id, plan_id, auto_renew=False):
        plan = MembershipPlan.query.get(plan_id)
        if not plan or not plan.is_active:
            return None, {"code": "NOT_FOUND", "message": "Plan not found or inactive"}

        # Check if user already has an active membership
        existing = Membership.query.filter_by(user_id=user_id, status='active').first()
        if existing:
            return None, {"code": "CONFLICT", "message": "User already has an active membership"}

        start_date = date.today()
        end_date = start_date + relativedelta(months=plan.duration_months)
        membership = Membership(
            user_id=user_id,
            plan_id=plan.id,
            club_id=plan.club_id,          # may be None
            status='active',
            start_date=start_date,
            end_date=end_date,
            auto_renew=auto_renew          # store the preference
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

    @staticmethod
    def get_active_membership_for_user(user_id):
        return Membership.query.filter_by(
            user_id=user_id, status='active'
        ).first()

    @staticmethod
    def seed_default_plans():
        """
        Inserts the 8 default membership plans (Standard & Premium,
        each with 1, 3, 6, 12 month durations) if they don't already exist.
        Safe to call multiple times (idempotent).
        """
        # This runs from create_app(), which can happen before the schema
        # exists (a fresh database awaiting `flask db upgrade`, or the test
        # suite, which calls db.create_all() after the app is built). Querying
        # a missing table raises and would take the whole app down, so skip.
        from sqlalchemy import inspect as sa_inspect

        try:
            if not sa_inspect(db.engine).has_table(MembershipPlan.__tablename__):
                return
        except Exception:
            return

        plans_data = [
            {"name": "Standard", "duration_months": 1,  "price": 499,  "discount_percentage": 50},
            {"name": "Standard", "duration_months": 3,  "price": 1299, "discount_percentage": 50},
            {"name": "Standard", "duration_months": 6,  "price": 2299, "discount_percentage": 50},
            {"name": "Standard", "duration_months": 12, "price": 3999, "discount_percentage": 50},
            {"name": "Premium",  "duration_months": 1,  "price": 999,  "discount_percentage": 100},
            {"name": "Premium",  "duration_months": 3,  "price": 2499, "discount_percentage": 100},
            {"name": "Premium",  "duration_months": 6,  "price": 4499, "discount_percentage": 100},
            {"name": "Premium",  "duration_months": 12, "price": 7999, "discount_percentage": 100},
        ]

        try:
            for plan_data in plans_data:
                existing = MembershipPlan.query.filter_by(
                    club_id=None,
                    name=plan_data["name"],
                    duration_months=plan_data["duration_months"],
                ).first()
                if not existing:
                    db.session.add(MembershipPlan(
                        club_id=None,
                        name=plan_data["name"],
                        price=plan_data["price"],
                        duration_months=plan_data["duration_months"],
                        discount_percentage=plan_data["discount_percentage"],
                        benefits=f"{plan_data['name']} membership for {plan_data['duration_months']} months",
                        is_active=True,
                    ))
            db.session.commit()
        except Exception:
            db.session.rollback()

