# JVCP — Japan ⇄ Vietnam Trusted Corridor Platform

A prototype digital-trust platform connecting Japanese and Vietnamese users through
verified identity, secure payments, and trusted cross-border services — built as a
portfolio project for the Product Engineering Internship at goen LLC (Tokyo).

The platform models what a real DID/VC-based identity layer, eKYC verification flow,
and QR/NFC payment rail could look like for cross-border commerce and travel between
Japan and Vietnam, with a tamper-evident audit trail underpinning every sensitive action.

## What's built

| Area | What it does |
|---|---|
| **Identity** | Registration + email verification, Google OAuth login, JWT auth, eKYC-style verification requests (document/selfie/DID-import), admin approval issuing a mock W3C-style Verifiable Credential, public credential verification endpoint, admin revocation |
| **Payments** | Order → Payment (QR code / NFC tap / card mock, real scannable QR) → Refund, fully scoped per user |
| **Marketplace & Providers** | Verified business directory with trust ratings and reviews, searchable marketplace |
| **Itinerary Planner** | Gemini-powered AI travel itinerary generation, structured day-by-day output |
| **Assistant** | Multilingual (VI/JA/EN) chat assistant, threaded conversations |
| **Remittance** | JP↔VN money transfer simulation with live-computed exchange rate and fee |
| **Audit Trail** | SHA-256 hash-chained, append-only event log covering identity, payment, and remittance actions; admin endpoint recomputes and verifies the full chain |
| **Admin Dashboard** | Aggregated acquisition/engagement/trust/commerce stats across the platform |

## Security work

This project treats security as a first-class deliverable, not an afterthought:

- **Rate-limited login** (`5/min` per IP) on the token endpoint, returning a proper
  `429 Too Many Requests` via a custom DRF exception handler — mitigates credential
  stuffing and brute-force attempts.
- **Object-level authorization (IDOR) audit**: every user-owned resource (orders,
  payments, refunds, remittances) is fetched via `get_object_or_404(Model, id=..,
  user=request.user)`, so a mismatched owner returns a clean `404` instead of leaking
  another user's data or throwing an unhandled server error.
- **Tamper-evident audit trail**: every identity/payment/remittance action is recorded
  as a hash-chained `AuditEvent` (each event's hash covers its own payload *and* the
  previous event's hash). An admin-only endpoint recomputes the entire chain and flags
  the exact event where tampering occurred, if any.
- **19 automated tests** covering registration validation, email verification, login
  throttling, the full VC issue/verify/revoke lifecycle, the complete pay/confirm/refund
  flow, a dedicated IDOR regression suite (proving an attacker account cannot view, pay,
  confirm, or refund another user's order), and audit-chain integrity including a test
  that deliberately corrupts an event and confirms detection.

See [`docs/TECHNICAL_REPORT.md`](docs/TECHNICAL_REPORT.md) for architecture details,
security design decisions, and known trade-offs / what's mocked vs. real.

## Stack

- **Backend:** Django 6.1, Django REST Framework, PostgreSQL, Redis, SimpleJWT,
  django-cors-headers, django-ratelimit, Google GenAI (Gemini)
- **Frontend:** React 19, Vite, React Router, Axios
- **Infra:** Docker Compose (backend, frontend, Postgres, Redis)

## Running locally

```bash
git clone <repo-url>
cd jvcp
cp .env.example .env   # fill in SECRET_KEY, GOOGLE_CLIENT_ID, LLM_API_KEY, email creds
docker compose up -d
```

- Backend API: `http://localhost:8001/api/v1/`
- Frontend: `http://localhost:5174`

Run the test suite:

```bash
docker compose exec backend python manage.py test identity payments core
```

## Notable endpoints

```
POST   /api/v1/auth/token/                      Login (rate-limited)
POST   /api/v1/identity/register/                Register
GET    /api/v1/identity/credentials/<id>/verify/ Public VC verification
POST   /api/v1/payments/orders/<id>/pay/         Pay an order
GET    /api/v1/audit/verify/                     Verify audit chain integrity (admin)
POST   /api/v1/remittance/quote/                 Get a JP↔VN transfer quote
```

## What's mocked vs. real

This is a prototype, not a production identity/payment system. The DID/VC layer,
eKYC document checks, QR/NFC payment confirmation, and remittance settlement are all
simulated — the architecture models the real shape (issuer/subject/claims/proof for
credentials; method/transaction/confirmation for payments) so it's swappable for a
real DID/VC provider, eKYC vendor, or payment processor later. See the technical
report for the full breakdown.

## Status / what's left

- Automated tests currently cover identity, payments, and the audit trail (the highest-risk
  surfaces); remittance, marketplace, providers, itineraries, and assistant do not yet have
  dedicated test coverage.
- Production deployment config (Gunicorn, Nginx, `docker-compose.prod.yml`) is documented
  in `infra/` but not deployed live.
