import pytest
from datetime import date
from dateutil.relativedelta import relativedelta
from app.memberships.models import MembershipPlan, Membership
from app.payments.models import Payment

@pytest.fixture
def sample_plan(sample_club, db_session):
    plan = MembershipPlan(
        club_id=sample_club.id,
        name="Gold Plan",
        duration_months=1, price=99.99,
        benefits="All access"
    )
    db_session.add(plan)
    db_session.commit()
    return plan

def test_get_plans(client, sample_plan, db_session):
    # With no club_id the endpoint returns the GLOBAL plans (club_id IS NULL),
    # so a club-scoped plan must not appear.
    response = client.get('/api/v1/memberships/plans')
    assert response.status_code == 200
    assert all(p['name'] != 'Gold Plan' for p in response.json)

    global_plan = MembershipPlan(
        club_id=None, name="Global Plan", duration_months=1,
        price=149.0, benefits="Everywhere",
    )
    db_session.add(global_plan)
    db_session.commit()

    response = client.get('/api/v1/memberships/plans')
    assert any(p['name'] == 'Global Plan' for p in response.json)

    # Filter by club_id returns that club's plan
    response = client.get(f'/api/v1/memberships/plans?club_id={sample_plan.club_id}')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['name'] == 'Gold Plan'

def test_subscribe_requires_payment_for_a_priced_plan(client, auth_headers,
                                                     sample_plan, db_session,
                                                     make_player):
    """A priced plan must not be granted to a caller who has not paid."""
    user = make_player(email="sub_unpaid@test.com")
    client.set_cookie('access_token_cookie', auth_headers(user))

    response = client.post('/api/v1/memberships/subscribe',
                           json={"plan_id": sample_plan.id})
    assert response.status_code == 402
    assert response.json['code'] == 'PAYMENT_REQUIRED'
    assert Membership.query.filter_by(user_id=user.id).count() == 0


def test_subscribe_success_after_payment(client, auth_headers, sample_plan,
                                         db_session, make_player):
    user = make_player(email="sub@test.com")
    db_session.add(Payment(
        user_id=user.id, amount=sample_plan.price, currency='INR',
        payment_type='membership', reference_id=sample_plan.id,
        status='completed', gateway_transaction_id='pi_test_paid',
    ))
    db_session.commit()

    client.set_cookie('access_token_cookie', auth_headers(user))
    response = client.post('/api/v1/memberships/subscribe',
                           json={"plan_id": sample_plan.id, "auto_renew": True})
    assert response.status_code == 201
    assert 'membership_id' in response.json

    membership = Membership.query.get(response.json['membership_id'])
    assert membership.auto_renew is True
    assert membership.status == 'active'


def test_subscribe_to_a_free_plan_needs_no_payment(client, auth_headers,
                                                   sample_club, db_session,
                                                   make_player):
    free_plan = MembershipPlan(club_id=sample_club.id, name="Trial",
                               duration_months=1, price=0, benefits="Taster")
    db_session.add(free_plan)
    db_session.commit()

    user = make_player(email="sub_free@test.com")
    client.set_cookie('access_token_cookie', auth_headers(user))

    response = client.post('/api/v1/memberships/subscribe',
                           json={"plan_id": free_plan.id})
    assert response.status_code == 201

def test_subscribe_conflict(client, auth_headers, sample_plan, db_session, make_player):
    user = make_player(email="sub_conflict@test.com")
    
    # Already subscribed
    membership = Membership(
        user_id=user.id,
        plan_id=sample_plan.id,
        club_id=sample_plan.club_id,
        status='active',
        start_date=date.today(),
        end_date=date.today() + relativedelta(months=1)
    )
    db_session.add(membership)
    db_session.commit()
    
    token = auth_headers(user)
    client.set_cookie('access_token_cookie', token)
    
    payload = {
        "plan_id": sample_plan.id
    }
    
    response = client.post('/api/v1/memberships/subscribe', json=payload)
    assert response.status_code == 409

def test_get_my_memberships(client, auth_headers, sample_plan, db_session, make_player):
    user = make_player(email="my_mems@test.com")
    membership = Membership(
        user_id=user.id,
        plan_id=sample_plan.id,
        club_id=sample_plan.club_id,
        status='active',
        start_date=date.today(),
        end_date=date.today() + relativedelta(months=1)
    )
    db_session.add(membership)
    db_session.commit()
    
    token = auth_headers(user)
    client.set_cookie('access_token_cookie', token)
    
    response = client.get('/api/v1/memberships/my-memberships')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['plan_name'] == 'Gold Plan'

def test_cancel_membership(client, auth_headers, sample_plan, db_session, make_player):
    user = make_player(email="cancel@test.com")
    membership = Membership(
        user_id=user.id,
        plan_id=sample_plan.id,
        club_id=sample_plan.club_id,
        status='active',
        start_date=date.today(),
        end_date=date.today() + relativedelta(months=1),
        auto_renew=True
    )
    db_session.add(membership)
    db_session.commit()
    
    token = auth_headers(user)
    client.set_cookie('access_token_cookie', token)
    
    response = client.post(f'/api/v1/memberships/{membership.id}/cancel')
    assert response.status_code == 200
    
    db_session.refresh(membership)
    assert membership.status == 'cancelled'
    assert membership.auto_renew is False
