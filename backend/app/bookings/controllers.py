from app.auth.decorators import role_required
from flask import Blueprint, request, jsonify
from app.extensions import db
from app.bookings.services import BookingService
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt

bookings_bp = Blueprint('bookings', __name__, url_prefix='/api/v1/bookings')

@bookings_bp.route('', methods=['POST'])
@role_required('player')
def create_booking():
    user_id = int(get_jwt_identity())
    data = request.get_json()

    court_id = data.get('court_id')
    booking_date = data.get('booking_date')
    start_time = data.get('start_time')
    end_time = data.get('end_time')

    if not all([court_id, booking_date, start_time, end_time]):
        return jsonify({"code": "VALIDATION_ERROR", "message": "Missing required fields"}), 400

    booking, error = BookingService.create_booking(user_id, court_id, booking_date, start_time, end_time)
    if error:
        status_code = 400
        if error['code'] == 'CONFLICT': status_code = 409
        elif error['code'] == 'NOT_FOUND': status_code = 404
        return jsonify(error), status_code

    return jsonify({
        "message": "Booking created successfully",
        "booking_id": booking.id
    }), 201

@bookings_bp.route('', methods=['GET'])
@role_required('player')
def get_my_bookings():
    user_id = int(get_jwt_identity())
    bookings = BookingService.get_my_bookings(user_id)

    from app.payments.models import Payment
    from flask import current_app
    from app.memberships.models import Membership

    base_fee = float(current_app.config.get("BOOKING_FEE", 500.0))
    membership = Membership.query.filter_by(user_id=user_id, status='active').first()
    discount = membership.plan.discount_percentage if membership and membership.plan else 0
    calculated_amount = round(base_fee * (1 - discount / 100.0), 2)

    booking_ids = [b.id for b in bookings]
    payments = {}
    if booking_ids:
        from app.payments.services import PaymentService
        for p in Payment.query.filter(
            Payment.payment_type == 'booking',
            Payment.reference_id.in_(booking_ids),
            Payment.user_id == user_id
        ).all():
            if p.status == 'pending' and p.gateway_transaction_id:
                PaymentService._reconcile_with_stripe(p)
                db.session.refresh(p)
            payments[p.reference_id] = p

    result = []
    for b in bookings:
        p = payments.get(b.id)
        result.append({
            "id": b.id,
            "court_id": b.court_id,
            "date": str(b.booking_date),
            "start_time": str(b.start_time),
            "end_time": str(b.end_time),
            "status": b.status,
            "court_name": b.court.name,
            "club_name": b.court.club.name,
            "sport_type": b.court.sport_type,
            "amount": float(p.amount) if p else float(calculated_amount),
            "payment_status": p.status if p else "pending"
        })
    return jsonify(result), 200

@bookings_bp.route('/<int:booking_id>/release', methods=['POST'])
@jwt_required()
def release_booking(booking_id):
    user_id = int(get_jwt_identity())
    success, error = BookingService.release_booking(user_id, booking_id)

    if error:
        status_code = 400
        if error['code'] == 'FORBIDDEN': status_code = 403
        elif error['code'] == 'NOT_FOUND': status_code = 404
        return jsonify(error), status_code

    return jsonify({"message": "Booking released successfully"}), 200


@bookings_bp.route('/club', methods=['GET'])
@role_required('owner', 'front-desk')
def get_club_bookings():
    """
    Bookings for the caller's club — the owner/front-desk view.

    Previously no such endpoint existed and GET /bookings was player-only, so
    owners and staff could not see any bookings at all.

    Optional query filters: ?date=YYYY-MM-DD&status=active&court_id=1
    """
    from app.clubs.models import Club

    user_id = int(get_jwt_identity())
    claims = get_jwt()

    if claims.get('role') == 'owner':
        club = Club.query.filter_by(owner_id=user_id).first()
    else:
        # Front-desk staff are not yet tied to a club in the data model, so
        # they operate on the club named by ?club_id=, falling back to the
        # single configured club.
        club_id = request.args.get('club_id', type=int)
        club = Club.query.get(club_id) if club_id else Club.query.first()

    if not club:
        return jsonify({"code": "NOT_FOUND", "message": "No club found for this user."}), 404

    bookings, error = BookingService.get_club_bookings(
        club_id=club.id,
        booking_date=request.args.get('date'),
        status=request.args.get('status'),
        court_id=request.args.get('court_id', type=int),
    )
    if error:
        return jsonify(error), 403 if error['code'] == 'FORBIDDEN' else 400

    # Payment state per booking, in one query rather than one per row.
    from app.payments.models import Payment

    booking_ids = [b.id for b in bookings]
    payment_by_booking = {}
    if booking_ids:
        for p in Payment.query.filter(
            Payment.payment_type == 'booking',
            Payment.reference_id.in_(booking_ids),
        ).order_by(Payment.created_at.asc()).all():
            # A later payment supersedes an earlier failed attempt.
            payment_by_booking[p.reference_id] = p

    result = []
    for b in bookings:
        payment = payment_by_booking.get(b.id)
        result.append({
            "id": b.id,
            "user_id": b.user_id,
            "member_name": b.user.name if b.user else None,
            "member_email": b.user.email if b.user else None,
            "member_phone": (b.user.phone or None) if b.user else None,
            "court_id": b.court_id,
            "court_name": b.court.name if b.court else None,
            "sport_type": b.court.sport_type if b.court else None,
            "club_name": club.name,
            "date": str(b.booking_date),
            "start_time": str(b.start_time),
            "end_time": str(b.end_time),
            "status": b.status,
            "created_at": str(b.created_at) if b.created_at else None,
            "payment_status": payment.status if payment else "unpaid",
            "payment_amount": payment.amount if payment else None,
        })

    return jsonify({"club": {"id": club.id, "name": club.name},
                    "count": len(result), "bookings": result}), 200
