from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from app.extensions import db
from app.memberships.models import MembershipPlan, Membership
from app.clubs.models import Club

def _plan_benefits(plan_data):
    """Human-readable summary shown on the pricing and checkout screens."""
    months = plan_data['duration_months']
    term = 'month' if months == 1 else 'year' if months == 12 else f'{months} months'
    return (f"{plan_data['discount_percentage']}% off court bookings, "
            f"billed every {term}")


class MembershipService:
    @staticmethod
    def get_plans(club_id=None):
        if not club_id:
            try:
                if MembershipPlan.query.filter_by(club_id=None).count() == 0:
                    MembershipService.seed_default_plans()
            except Exception:
                pass

        query = MembershipPlan.query.filter_by(is_active=True)
        if club_id:
            query = query.filter_by(club_id=club_id)
        else:
            # Global plans (club_id IS NULL)
            query = query.filter_by(club_id=None)
        return query.order_by(MembershipPlan.name, MembershipPlan.duration_months).all()

    @staticmethod
    def subscribe(user_id, plan_id, auto_renew=False):
        try:
            db.create_all()
        except Exception:
            pass

        try:
            # Ensure plans are seeded
            if MembershipPlan.query.count() == 0:
                MembershipService.seed_default_plans()

            plan = MembershipPlan.query.get(plan_id)
            if not plan:
                plan = MembershipPlan.query.filter_by(is_active=True).first()

            if not plan or not plan.is_active:
                return None, {"code": "NOT_FOUND", "message": "Plan not found or inactive"}

            # Check if user already has an active membership
            existing = Membership.query.filter_by(user_id=user_id, status='active').first()
            if existing:
                return None, {"code": "CONFLICT", "message": "User already has an active membership"}

            # A priced plan is only granted once it has actually been paid for.
            if (plan.price or 0) > 0:
                from app.payments.services import PaymentService
                if not PaymentService.settle(user_id, 'membership', plan.id):
                    return None, {"code": "PAYMENT_REQUIRED",
                                  "message": "Payment for this plan has not been completed."}

            start_date = date.today()
            duration = getattr(plan, 'duration_months', 1) or 1
            end_date = start_date + relativedelta(months=duration)
            membership = Membership(
                user_id=user_id,
                plan_id=plan.id,
                club_id=plan.club_id,          # may be None
                status='active',
                start_date=start_date,
                end_date=end_date,
                auto_renew=bool(auto_renew)
            )
            db.session.add(membership)
            db.session.commit()
            return membership, None
        except Exception as e:
            db.session.rollback()
            return None, {"code": "DATABASE_ERROR", "message": f"Failed to save membership: {str(e)}"}

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
        try:
            db.create_all()
        except Exception:
            pass

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
            MembershipService._seed_plans(plans_data)
        except Exception:
            # Schema is behind the models (e.g. a pending migration). Seeding is
            # best-effort: swallowing this keeps the app importable so that
            # `flask db upgrade` can actually be run.
            db.session.rollback()

    @staticmethod
    def _seed_plans(plans_data):
        for plan_data in plans_data:
            existing = MembershipPlan.query.filter_by(
                club_id=None,
                name=plan_data["name"],
                duration_months=plan_data["duration_months"],
            ).first()
            if existing is None:
                db.session.add(MembershipPlan(
                    club_id=None,
                    name=plan_data["name"],
                    price=plan_data["price"],
                    duration_months=plan_data["duration_months"],
                    discount_percentage=plan_data["discount_percentage"],
                    benefits=_plan_benefits(plan_data),
                    is_active=True,
                ))
            else:
                # Keep price, discount and copy in step with this table on every
                # boot; a database seeded by an older build otherwise keeps
                # advertising stale terms on the public pricing page.
                existing.price = plan_data["price"]
                existing.discount_percentage = plan_data["discount_percentage"]
                existing.benefits = _plan_benefits(plan_data)
        db.session.commit()
