"""
The demo seeder must be self-contained: everything it creates lives in the
database and `wipe-demo` must remove all of it, leaving real accounts and the
reference membership plans alone.
"""
from app.auth.models import User
from app.attendance.models import AttendanceRecord
from app.bookings.models import Booking, CourtBlock
from app.clubs.models import Club, Court
from app.events.models import Event, EventRegistration
from app.memberships.models import Membership, MembershipPlan
from app.notifications.models import Notification
from app.payments.models import Payment

DEMO_DOMAIN = "@demo.clubeon.test"


def _seed(app, **kwargs):
    args = ["seed-demo", "--months", "2", "--members", "8"]
    for key, value in kwargs.items():
        args += [f"--{key.replace('_', '-')}", str(value)]
    return app.test_cli_runner().invoke(args=args)


from sqlalchemy import or_

def test_seed_demo_populates_every_table(app):
    result = _seed(app)
    assert result.exit_code == 0, result.output

    assert User.query.filter(
        or_(
            User.email.like(f"%{DEMO_DOMAIN}"),
            User.email.in_(["admin@gmail.com", "staff@gmail.com"])
        )
    ).count() == 11  # 8 members + 1 owner (admin@gmail.com) + 2 staff (staff@gmail.com + frontdesk2)
    assert Club.query.count() == 2
    assert Court.query.count() > 0
    assert Booking.query.count() > 0
    assert Payment.query.count() > 0
    assert Membership.query.count() > 0
    assert Event.query.count() > 0
    assert EventRegistration.query.count() > 0
    assert AttendanceRecord.query.count() > 0
    assert Notification.query.count() > 0
    assert CourtBlock.query.count() > 0


def test_seed_demo_is_deterministic(app):
    _seed(app)
    first = Booking.query.count()

    app.test_cli_runner().invoke(args=["wipe-demo"])
    _seed(app)

    assert Booking.query.count() == first


def test_seed_demo_refuses_to_double_seed_without_force(app):
    assert _seed(app).exit_code == 0
    result = _seed(app)
    assert result.exit_code != 0
    assert "already exist" in result.output


def test_wipe_demo_removes_everything_it_created(app):
    _seed(app)
    result = app.test_cli_runner().invoke(args=["wipe-demo"])
    assert result.exit_code == 0, result.output

    assert User.query.count() == 0
    assert Club.query.count() == 0
    assert Court.query.count() == 0
    assert Booking.query.count() == 0
    assert Payment.query.count() == 0
    assert Membership.query.count() == 0
    assert Event.query.count() == 0
    assert EventRegistration.query.count() == 0
    assert AttendanceRecord.query.count() == 0
    assert Notification.query.count() == 0
    assert CourtBlock.query.count() == 0

    # Reference data is not demo data and must survive.
    assert MembershipPlan.query.count() > 0


def test_wipe_demo_leaves_real_accounts_alone(app, make_player):
    real = make_player(email="real.person@example.com")
    _seed(app)
    app.test_cli_runner().invoke(args=["wipe-demo"])

    assert User.query.filter_by(email="real.person@example.com").count() == 1
    assert User.query.get(real.id) is not None
