"""
Flask CLI commands.

Anything that writes to the database lives here rather than in create_app().
create_app() runs on every boot — including against production — so seeding
from it silently injects rows into whatever DATABASE_URL points at. These
commands are explicit and safe to re-run.

    flask seed-plans   # membership plans (reference data, required)
    flask seed-demo    # a full demo club with months of history
    flask wipe-demo    # remove everything seed-demo created
"""
import random
from datetime import date, datetime, time, timedelta

import click
from dateutil.relativedelta import relativedelta
from flask import current_app
from flask.cli import with_appcontext

from app.extensions import db


def register_cli(app):
    app.cli.add_command(seed_plans)
    app.cli.add_command(seed_demo)
    app.cli.add_command(wipe_demo)


# ---------------------------------------------------------------------------
# Membership plans (reference data)
# ---------------------------------------------------------------------------
@click.command("seed-plans")
@with_appcontext
def seed_plans():
    """Insert/refresh the default membership plans. Idempotent."""
    from app.memberships.services import MembershipService

    MembershipService.seed_default_plans()
    db.session.commit()
    click.echo("Membership plans seeded.")


# ---------------------------------------------------------------------------
# Demo data
# ---------------------------------------------------------------------------
# Every demo account uses this domain, which is what wipe-demo keys off. Real
# accounts are never touched.
DEMO_DOMAIN = "@demo.clubeon.test"
DEMO_PASSWORD = "Demo@12345"
DEMO_ADMIN_EMAIL = "admin@gmail.com"
DEMO_STAFF_EMAIL = "staff@gmail.com"

FIRST_NAMES = [
    "Aarav", "Ananya", "Rohan", "Priya", "Vikram", "Meera", "Arjun", "Kavya",
    "Aditya", "Ishita", "Karan", "Sneha", "Rahul", "Divya", "Siddharth",
    "Nisha", "Manish", "Pooja", "Varun", "Riya", "Ajay", "Tara", "Nikhil",
    "Sanya", "Rajat", "Anjali", "Dev", "Neha", "Kabir", "Simran", "Yash",
    "Aisha", "Harsh", "Lakshmi", "Om", "Trisha", "Zain", "Bhavna", "Farhan",
    "Gauri",
]
LAST_NAMES = [
    "Sharma", "Patel", "Reddy", "Nair", "Iyer", "Singh", "Gupta", "Mehta",
    "Rao", "Desai", "Kulkarni", "Banerjee", "Chopra", "Malhotra", "Joshi",
    "Verma", "Bose", "Kapoor", "Menon", "Pillai",
]

# (name, sport, active)
COURT_PLAN = [
    ("Centre Court", "tennis", True),
    ("Court 2 - Clay", "tennis", True),
    ("Badminton Hall A", "badminton", True),
    ("Badminton Hall B", "badminton", True),
    ("Squash Box 1", "squash", True),
    ("Squash Box 2", "squash", False),
    ("Indoor Basketball", "basketball", True),
    ("Rooftop Pickleball", "pickleball", True),
]

EVENT_PLAN = [
    ("Summer Open Doubles", "Club-wide doubles tournament across all badminton halls.",
     "badminton", 32, 500.0),
    ("Junior Coaching Clinic", "Six-week coaching block for under-14 players.",
     "tennis", 24, 1200.0),
    ("Corporate League Night", "Round-robin evening league for member companies.",
     "squash", 16, 750.0),
    ("Community Open Day", "Free taster sessions on every court. All welcome.",
     "multi-purpose", 60, 0.0),
    ("Monsoon Smash Championship", "Knockout singles championship with trophies.",
     "badminton", 32, 650.0),
    ("Sunrise Fitness Bootcamp", "Early-morning conditioning on the indoor court.",
     "basketball", 20, 300.0),
]

ANNOUNCEMENTS = [
    ("Court resurfacing on Squash Box 2",
     "Squash Box 2 is closed this fortnight for panel replacement and floor "
     "sanding. Squash Box 1 remains open and bookable as usual.", "maintenance"),
    ("Registrations open: Monsoon Smash Championship",
     "Singles knockout brackets are now open to all members. Entry includes "
     "match shuttles and a group-stage guarantee.", "tournament"),
    ("Updated peak-hour booking policy",
     "Weekday evening slots between 18:00 and 21:00 are now limited to two per "
     "member per week so more players get court time.", "policy"),
    ("New LED floodlights on Centre Court",
     "Centre Court has been re-lit to tournament specification. Evening play "
     "resumes from this weekend.", "broadcast"),
]


def _rng():
    """Deterministic RNG so a reseed produces the same figures in a demo."""
    return random.Random(20260096)


def _make_user(name, email, role, rng, created_at):
    from app.auth.models import User

    user = User(
        name=name,
        email=email,
        role=role,
        phone=f"+9198{rng.randint(10000000, 99999999)}",
        created_at=created_at,
        gender=rng.choice(["Male", "Female", "Other", "Prefer not to say"]),
        dob=date(rng.randint(1975, 2007), rng.randint(1, 12), rng.randint(1, 28)),
        address=f"{rng.randint(1, 220)} {rng.choice(['MG Road', 'Lake View Rd', '4th Cross', 'Church St', 'Residency Rd'])}, Bengaluru",
        notify_email=True,
        notify_sms=rng.random() < 0.4,
        notify_push=rng.random() < 0.8,
        profile_public=rng.random() < 0.3,
    )
    user.set_password(DEMO_PASSWORD)
    db.session.add(user)
    return user


@click.command("seed-demo")
@click.option("--months", default=8, show_default=True,
              help="How many months of history to generate.")
@click.option("--members", default=60, show_default=True,
              help="How many demo players to create.")
@click.option("--force", is_flag=True,
              help="Wipe existing demo data first instead of refusing.")
@with_appcontext
def seed_demo(months, members, force):
    """
    Build a complete demo club: staff, members, courts, months of bookings,
    memberships, payments, events, attendance and announcements.

    Everything lives in the database, so `flask wipe-demo` — or dropping the
    database — removes all of it. Demo accounts all use the
    @demo.clubeon.test domain and log in with the same password.
    """
    from app.auth.models import User
    from app.attendance.models import AttendanceRecord
    from app.bookings.models import Booking, CourtBlock
    from app.clubs.models import Club, Court
    from app.events.models import Event, EventRegistration
    from app.memberships.models import Membership, MembershipPlan
    from app.memberships.services import MembershipService
    from app.notifications.models import Notification
    from app.payments.models import Payment

    if current_app.config.get("ENV") == "production" or \
            current_app.config.get("FLASK_ENV") == "production":
        raise click.ClickException("Refusing to seed demo data in production.")

    from sqlalchemy import or_
    existing = User.query.filter(
        or_(
            User.email.like(f"%{DEMO_DOMAIN}"),
            User.email.in_([DEMO_ADMIN_EMAIL, DEMO_STAFF_EMAIL])
        )
    ).count()
    if existing and not force:
        raise click.ClickException(
            f"{existing} demo accounts already exist. Re-run with --force to "
            "replace them, or run `flask wipe-demo` first.")
    if existing:
        _wipe(quiet=True)

    rng = _rng()
    today = date.today()
    history_start = today - relativedelta(months=months)

    # Plans must exist before memberships reference them.
    MembershipService.seed_default_plans()
    plans = MembershipPlan.query.filter_by(club_id=None, is_active=True).all()
    if not plans:
        raise click.ClickException("No membership plans found; run `flask seed-plans`.")
    plans_by_name = {}
    for plan in plans:
        plans_by_name.setdefault(plan.name, []).append(plan)

    # ---------------------------------------------------------------- people
    owner = _make_user("Meera Krishnan", DEMO_ADMIN_EMAIL, "owner", rng,
                       datetime.combine(history_start, time(9, 0)))
    staff = [
        _make_user("Rajesh Kumar", DEMO_STAFF_EMAIL, "front-desk", rng,
                   datetime.combine(history_start, time(9, 30))),
        _make_user("Fatima Sheikh", f"frontdesk2{DEMO_DOMAIN}", "front-desk", rng,
                   datetime.combine(history_start, time(9, 45))),
    ]
    db.session.flush()

    # Draw distinct first/last pairs from the full product so no two demo
    # members share a name — indexing by a fixed stride wrapped and produced
    # duplicates once the member count passed the first-name list length.
    name_pool = [(f, l) for f in FIRST_NAMES for l in LAST_NAMES]
    rng.shuffle(name_pool)
    if members > len(name_pool):
        raise click.ClickException(
            f"--members cannot exceed {len(name_pool)} distinct names.")

    players = []
    for i, (first, last) in enumerate(name_pool[:members]):
        email = f"{first}.{last}".lower() + DEMO_DOMAIN
        joined = history_start + timedelta(days=rng.randint(0, months * 30 - 1))
        players.append(_make_user(f"{first} {last}", email, "player", rng,
                                  datetime.combine(joined, time(rng.randint(8, 20), 0))))
    db.session.flush()

    # ----------------------------------------------------------------- clubs
    club = Club(
        name="Ace Sports Club",
        address="42 Residency Road, Bengaluru 560025",
        owner_id=owner.id,
        open_time="06:00",
        close_time="22:00",
        slot_duration_minutes=60,
        latitude=12.9716,
        longitude=77.5946,
        amenities=["parking", "cafe", "locker-room", "pro-shop", "wifi", "showers"],
        tags=["family-friendly", "indoor", "air-conditioned", "floodlit"],
    )
    db.session.add(club)
    db.session.flush()

    courts = []
    for name, sport, active in COURT_PLAN:
        court = Court(
            club_id=club.id, name=name, sport_type=sport, is_active=active,
            amenities=["led-lighting", "wooden-flooring"] if sport == "badminton"
            else ["floodlit", "all-weather"],
            tags=["kid-friendly"] if sport in ("badminton", "pickleball") else ["pro-training"],
        )
        db.session.add(court)
        courts.append(court)
    db.session.flush()
    bookable = [c for c in courts if c.is_active]

    # A second club so the staff club picker and the public directory have a
    # real choice to make.
    aqua = Club(
        name="AquaFit Olympic & Wellness Club",
        address="12 Lake View Rd, Indiranagar, Bengaluru 560038",
        owner_id=owner.id,
        open_time="06:00", close_time="22:00", slot_duration_minutes=60,
        latitude=12.9784, longitude=77.6408,
        amenities=["chlorine-free", "heated", "parking", "cafe", "showers", "sauna"],
        tags=["kid-friendly", "family-friendly", "wellness"],
    )
    db.session.add(aqua)
    db.session.flush()
    db.session.add_all([
        Court(club_id=aqua.id, name="Olympic Lap Pool (50m)", sport_type="swimming",
              is_active=True, amenities=["chlorine-free", "heated", "lane-dividers"],
              tags=["pro-training"]),
        Court(club_id=aqua.id, name="Learners & Kids Splash Pool", sport_type="swimming",
              is_active=True, amenities=["chlorine-free", "shallow-depth", "lifeguard-on-duty"],
              tags=["kid-friendly", "family-friendly"]),
    ])

    # ----------------------------------------------------------- memberships
    # Roughly half the players hold a plan; a few have lapsed or cancelled.
    payments = []
    membership_holders = rng.sample(players, k=int(members * 0.55))
    for user in membership_holders:
        tier = "Premium" if rng.random() < 0.35 else "Standard"
        plan = rng.choice(plans_by_name[tier])
        start = user.created_at.date() + timedelta(days=rng.randint(0, 20))
        if start > today:
            start = today
        end = start + relativedelta(months=plan.duration_months)

        roll = rng.random()
        if end < today:
            status = "expired"
        elif roll < 0.08:
            status = "cancelled"
        else:
            status = "active"

        db.session.add(Membership(
            user_id=user.id, plan_id=plan.id, club_id=None, status=status,
            start_date=start, end_date=end, auto_renew=rng.random() < 0.45,
            created_at=datetime.combine(start, time(11, 0)),
        ))
        payments.append(Payment(
            user_id=user.id, amount=plan.price, currency="INR",
            payment_type="membership", reference_id=plan.id, status="completed",
            gateway_transaction_id=f"pi_demo_mem_{user.id}",
            created_at=datetime.combine(start, time(11, 0)),
        ))

    # -------------------------------------------------------------- bookings
    # Weekday evenings and weekend mornings are busiest, which is what makes
    # the occupancy heatmap and peak-hour KPI meaningful.
    PEAK_EVENING = [18, 19, 20]
    WEEKEND_MORNING = [7, 8, 9, 10]
    OFF_PEAK = [6, 11, 12, 13, 14, 15, 16, 17, 21]

    bookings = []
    day = history_start
    while day <= today + timedelta(days=14):
        is_weekend = day.weekday() >= 5
        # Volume grows over the period so the trend chart has a shape.
        progress = (day - history_start).days / max((today - history_start).days, 1)
        base_volume = 6 + int(progress * 10)
        volume = rng.randint(base_volume, base_volume + 6)
        if is_weekend:
            volume += 4
        if day > today:
            volume = max(volume // 3, 2)  # fewer forward bookings

        taken = set()
        for _ in range(volume):
            court = rng.choice(bookable)
            if is_weekend:
                hour = rng.choice(WEEKEND_MORNING * 3 + PEAK_EVENING * 2 + OFF_PEAK)
            else:
                hour = rng.choice(PEAK_EVENING * 4 + OFF_PEAK + WEEKEND_MORNING)
            if (court.id, hour) in taken:
                continue
            taken.add((court.id, hour))

            if day < today:
                status = "active"
                roll = rng.random()
                if roll < 0.07:
                    status = "released"
                elif roll < 0.09:
                    status = "overridden"
            else:
                status = "released" if rng.random() < 0.05 else "active"

            booking = Booking(
                user_id=rng.choice(players).id,
                court_id=court.id,
                booking_date=day,
                start_time=time(hour, 0),
                end_time=time(hour + 1, 0),
                status=status,
                is_peak_hour=hour in PEAK_EVENING,
                created_at=datetime.combine(day - timedelta(days=rng.randint(1, 6)),
                                            time(rng.randint(9, 21), rng.randint(0, 59))),
            )
            db.session.add(booking)
            bookings.append(booking)
        day += timedelta(days=1)
    db.session.flush()

    # Court fees. Members with an active plan pay a discounted rate, which is
    # what the booking flow itself charges.
    active_member_ids = {
        m.user_id for m in Membership.query.filter_by(status="active").all()
    }
    base_fee = float(current_app.config.get("BOOKING_FEE", 500.0))
    for booking in bookings:
        if booking.status != "active" or booking.booking_date > today:
            continue
        discounted = booking.user_id in active_member_ids
        amount = round(base_fee * (0.5 if discounted else 1.0), 2)
        if amount <= 0:
            continue
        roll = rng.random()
        status = "completed" if roll < 0.94 else ("pending" if roll < 0.98 else "failed")
        payments.append(Payment(
            user_id=booking.user_id, amount=amount, currency="INR",
            payment_type="booking", reference_id=booking.id, status=status,
            gateway_transaction_id=f"pi_demo_bk_{booking.id}",
            created_at=datetime.combine(booking.booking_date, booking.start_time)
            - timedelta(hours=rng.randint(2, 72)),
        ))

    # ---------------------------------------------------------------- events
    events = []
    for i, (title, description, _sport, capacity, fee) in enumerate(EVENT_PLAN):
        # Spread across the window: the first few are past, the rest upcoming.
        offset_days = int((i / max(len(EVENT_PLAN) - 1, 1)) * (months * 30 + 40)) \
            - months * 30 + 20
        event_date = today + timedelta(days=offset_days)
        start_hour = rng.choice([7, 9, 17, 18])
        event = Event(
            club_id=club.id,
            created_by=owner.id,
            title=title,
            description=description,
            event_date=event_date,
            start_time=time(start_hour, 0),
            end_time=time(min(start_hour + 3, 23), 0),
            max_attendees=capacity,
            registration_fee=fee,
            status="completed" if event_date < today else "upcoming",
            created_at=datetime.combine(event_date - timedelta(days=21), time(10, 0)),
        )
        db.session.add(event)
        events.append(event)
    db.session.flush()

    for event in events:
        fill = rng.uniform(0.45, 0.95)
        attendees = rng.sample(players, k=min(int(event.max_attendees * fill), len(players)))
        for user in attendees:
            cancelled = rng.random() < 0.06
            db.session.add(EventRegistration(
                event_id=event.id, user_id=user.id,
                status="cancelled" if cancelled else "registered",
                registered_at=datetime.combine(
                    event.event_date - timedelta(days=rng.randint(2, 20)), time(12, 0)),
            ))
            if event.registration_fee > 0 and not cancelled:
                payments.append(Payment(
                    user_id=user.id, amount=event.registration_fee, currency="INR",
                    payment_type="event", reference_id=event.id, status="completed",
                    gateway_transaction_id=f"pi_demo_ev_{event.id}_{user.id}",
                    created_at=datetime.combine(
                        event.event_date - timedelta(days=rng.randint(2, 20)), time(12, 5)),
                ))

    db.session.add_all(payments)

    # ------------------------------------------------------------ attendance
    # Most past bookings were honoured; some were no-shows.
    for booking in bookings:
        if booking.status != "active" or booking.booking_date >= today:
            continue
        if rng.random() < 0.18:
            continue  # no-show
        check_in = datetime.combine(booking.booking_date, booking.start_time) \
            - timedelta(minutes=rng.randint(0, 12))
        record = AttendanceRecord(
            user_id=booking.user_id, booking_id=booking.id, check_in_at=check_in,
        )
        if rng.random() < 0.9:
            record.check_out_at = check_in + timedelta(minutes=rng.randint(55, 95))
        db.session.add(record)

    # Today's arrivals: a few already checked in, the rest still expected, so
    # the front-desk screens have something live to show.
    todays = [b for b in bookings if b.booking_date == today and b.status == "active"]
    for booking in todays[: max(len(todays) // 3, 1)]:
        db.session.add(AttendanceRecord(
            user_id=booking.user_id, booking_id=booking.id,
            check_in_at=datetime.combine(today, booking.start_time),
        ))

    # --------------------------------------------------------- court blocks
    db.session.add(CourtBlock(
        court_id=next(c.id for c in courts if c.name == "Squash Box 2"),
        start_date=today - timedelta(days=3),
        end_date=today + timedelta(days=11),
        title="Panel replacement and floor sanding",
        created_by=owner.id,
    ))

    # -------------------------------------------------------- announcements
    audience = [owner] + staff + players
    for i, (title, body, kind) in enumerate(ANNOUNCEMENTS):
        published = datetime.combine(today - timedelta(days=(i + 1) * 4), time(10, 0))
        for user in audience:
            db.session.add(Notification(
                user_id=user.id, title=title, body=body, type=kind,
                is_read=rng.random() < 0.55, created_at=published,
            ))

    db.session.commit()

    from sqlalchemy import or_
    counts = {
        "users": User.query.filter(
            or_(
                User.email.like(f"%{DEMO_DOMAIN}"),
                User.email.in_([DEMO_ADMIN_EMAIL, DEMO_STAFF_EMAIL])
            )
        ).count(),
        "clubs": 2,
        "courts": len(COURT_PLAN) + 2,
        "bookings": len(bookings),
        "memberships": len(membership_holders),
        "payments": len(payments),
        "events": len(events),
        "registrations": EventRegistration.query.count(),
        "attendance": AttendanceRecord.query.count(),
        "notifications": Notification.query.count(),
    }
    click.echo("Demo data created:")
    for key, value in counts.items():
        click.echo(f"  {value:>6}  {key}")
    click.echo("")
    click.echo(f"  Owner       {DEMO_ADMIN_EMAIL}")
    click.echo(f"  Front desk  {DEMO_STAFF_EMAIL}")
    click.echo(f"  Member      {players[0].email}")
    click.echo(f"  Password    {DEMO_PASSWORD}")
    click.echo("")
    click.echo("Remove it all with: flask wipe-demo")


# ---------------------------------------------------------------------------
# Teardown
# ---------------------------------------------------------------------------
def _wipe(quiet=False):
    """
    Delete everything seed-demo created.

    Demo users are identified by their email domain or admin/staff emails;
    every other row is reached through them, so nothing belonging to a real
    account is touched.
    """
    from app.auth.models import User
    from app.attendance.models import AttendanceRecord
    from app.bookings.models import Booking, BookingIntent, CourtBlock
    from app.clubs.models import Club, Court
    from app.events.models import Event, EventRegistration
    from app.memberships.models import Membership
    from app.notifications.models import Notification
    from app.payments.models import Payment
    from sqlalchemy import or_

    demo_users = User.query.filter(
        or_(
            User.email.like(f"%{DEMO_DOMAIN}"),
            User.email.in_([DEMO_ADMIN_EMAIL, DEMO_STAFF_EMAIL])
        )
    ).all()
    if not demo_users:
        if not quiet:
            click.echo("No demo data found.")
        return 0

    user_ids = [u.id for u in demo_users]
    club_ids = [c.id for c in Club.query.filter(Club.owner_id.in_(user_ids)).all()]
    court_ids = [c.id for c in Court.query.filter(Court.club_id.in_(club_ids)).all()] \
        if club_ids else []
    event_ids = [e.id for e in Event.query.filter(Event.club_id.in_(club_ids)).all()] \
        if club_ids else []
    booking_ids = [b.id for b in Booking.query.filter(
        Booking.user_id.in_(user_ids)).all()]

    # Children first: these tables carry the foreign keys.
    if booking_ids or user_ids:
        AttendanceRecord.query.filter(
            AttendanceRecord.user_id.in_(user_ids)).delete(synchronize_session=False)
    if event_ids:
        EventRegistration.query.filter(
            EventRegistration.event_id.in_(event_ids)).delete(synchronize_session=False)
    EventRegistration.query.filter(
        EventRegistration.user_id.in_(user_ids)).delete(synchronize_session=False)
    Payment.query.filter(Payment.user_id.in_(user_ids)).delete(synchronize_session=False)
    Membership.query.filter(Membership.user_id.in_(user_ids)).delete(synchronize_session=False)
    Notification.query.filter(Notification.user_id.in_(user_ids)).delete(synchronize_session=False)
    BookingIntent.query.filter(BookingIntent.user_id.in_(user_ids)).delete(synchronize_session=False)
    Booking.query.filter(Booking.user_id.in_(user_ids)).delete(synchronize_session=False)
    if court_ids:
        Booking.query.filter(Booking.court_id.in_(court_ids)).delete(synchronize_session=False)
        CourtBlock.query.filter(CourtBlock.court_id.in_(court_ids)).delete(synchronize_session=False)
    CourtBlock.query.filter(CourtBlock.created_by.in_(user_ids)).delete(synchronize_session=False)
    if event_ids:
        AttendanceRecord.query.filter(
            AttendanceRecord.event_id.in_(event_ids)).delete(synchronize_session=False)
        Event.query.filter(Event.id.in_(event_ids)).delete(synchronize_session=False)
    if court_ids:
        Court.query.filter(Court.id.in_(court_ids)).delete(synchronize_session=False)
    if club_ids:
        Club.query.filter(Club.id.in_(club_ids)).delete(synchronize_session=False)
    User.query.filter(User.id.in_(user_ids)).delete(synchronize_session=False)

    db.session.commit()
    return len(user_ids)


@click.command("wipe-demo")
@with_appcontext
def wipe_demo():
    """Remove every row seed-demo created. Real accounts are untouched."""
    removed = _wipe()
    if removed:
        click.echo(f"Removed {removed} demo accounts and all their data.")
