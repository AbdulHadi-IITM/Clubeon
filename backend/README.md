# Clubeon — Backend

Flask modular monolith serving the Clubeon API at `/api/v1`. Interactive docs
at `/api/docs`, liveness at `/health`.

## Running locally

```bash
python -m venv .venv && .venv/bin/pip install -r requirements.txt
cp .env.example .env          # then fill in DATABASE_URL, SECRET_KEY, JWT_SECRET_KEY
.venv/bin/flask db upgrade    # create/patch the schema — required
.venv/bin/python run.py
```

The API listens on `PORT` (default 5000). The Vite dev server proxies `/api`
there, so start the backend before `npm run dev` in `../Frontend`.

## Schema

Alembic owns the schema. `create_app()` does **not** call `db.create_all()` and
does **not** insert demo rows — it used to do both on every boot, which wrote
fixture data into whatever database `DATABASE_URL` pointed at, production
included. After pulling changes that touch models:

```bash
.venv/bin/flask db upgrade
```

Membership plans are reference data the app needs to function, so they are
seeded (idempotently) on startup and kept in step with `MembershipService`'s
plan table. You can also run it explicitly:

```bash
.venv/bin/flask seed-plans
```

### Demo data

Demo content is opt-in and never runs by itself. It builds a complete club —
owner, front-desk staff, members, courts, months of bookings, memberships,
payments, events, registrations, attendance and announcements — so every
dashboard has real figures to show:

```bash
.venv/bin/flask seed-demo                       # 8 months, 60 members
.venv/bin/flask seed-demo --months 12 --members 120
.venv/bin/flask seed-demo --force               # replace an existing demo set
```

It is deterministic, so reseeding reproduces the same numbers. Every demo
account lives on `@demo.clubeon.test` and signs in with `Demo@12345`:

| Role       | Email                          |
|------------|--------------------------------|
| Owner      | `admin@gmail.com`              |
| Front desk | `staff@gmail.com`              |
| Member     | printed by the command         |

All of it is database rows — nothing is cached in the browser — so it comes out
cleanly:

```bash
.venv/bin/flask wipe-demo    # removes only demo rows; real accounts untouched
```

Dropping the database removes it too. The command refuses to run with
`FLASK_ENV=production`.

## Tests

```bash
.venv/bin/python -m pytest -q
```

They run against in-memory SQLite and create their own schema, so no database
setup is needed.

## Payments

Checkout is Stripe-only and **fails closed**: with no `STRIPE_SECRET_KEY` the
payment endpoints return 503 and the UI says payments are unavailable. There is
deliberately no offline/mock fallback — the previous one granted memberships
and event seats without taking money whenever Stripe was unreachable.

Fulfilment is gated on settlement, not on the client's say-so:

- `POST /memberships/subscribe` and `POST /events/<id>/register` refuse with
  **402 PAYMENT_REQUIRED** unless a completed `Payment` exists for that
  plan/event (free plans and free events are unaffected).
- `PaymentService.settle()` reconciles a still-pending PaymentIntent directly
  with Stripe, so the flow works before the webhook lands and in environments
  with no webhook configured.
- The only webhook is the signature-verified `POST /payments/stripe/webhook`.
  The old unauthenticated `POST /payments/webhook` accepted an unsigned body
  and marked any payment completed; it has been removed.

For local webhook delivery:

```bash
stripe listen --forward-to localhost:5000/api/v1/payments/stripe/webhook
```

## Production checklist

- `FLASK_ENV=production` — the app refuses to start on the default development
  secrets.
- `SECRET_KEY` and `JWT_SECRET_KEY` set to strong random values
  (`python -c "import secrets;print(secrets.token_urlsafe(48))"`).
- `JWT_COOKIE_SECURE=True` once served over HTTPS.
- `CORS_ORIGINS` set to the real frontend origin, not `*`.
- `FLASK_DEBUG` unset — the Werkzeug debugger executes arbitrary code.
- Serve through a WSGI server (gunicorn/uwsgi), not `run.py`.
- `.env` is gitignored and must never be committed.
