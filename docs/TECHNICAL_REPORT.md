# JVCP — Technical Report

## Japan ⇄ Vietnam Trusted Corridor Platform

### Product Engineering Internship Portfolio Project

---

## 1. Executive Summary

JVCP is a prototype digital-trust platform designed around cross-border interactions between Japanese and Vietnamese users.

The platform combines digital identity, eKYC-style verification, Verifiable Credentials, secure payment workflows, marketplace services, travel assistance, remittance simulation, and a tamper-evident audit trail.

The objective is not to implement a production banking, identity, or government-verification system. Instead, JVCP models the architecture and user flows that could support such a platform, while keeping external identity providers, KYC vendors, payment processors, and settlement infrastructure replaceable.

The project was designed with security, privacy, object-level authorization, auditability, and extensibility as first-class engineering concerns.

---

## 2. Problem Statement

Cross-border travel and commerce require users to repeatedly establish identity, trust merchants, make payments, and communicate across different countries and systems.

A trusted digital corridor could reduce this friction by providing:

- reusable digital identity;
- verifiable credentials;
- identity verification workflows;
- trusted providers;
- secure transaction flows;
- cross-border payment and remittance interfaces;
- multilingual assistance;
- auditable transaction records.

JVCP explores how these components could be combined into one service.

---

## 3. Project Objectives

The main objectives are:

1. Build a digital identity layer.
2. Provide email and Google-based authentication.
3. Model an eKYC verification workflow.
4. Model DID and Verifiable Credential issuance.
5. Provide public credential verification.
6. Provide secure user-scoped payment workflows.
7. Support QR, NFC and card payment prototypes.
8. Provide marketplace and verified-provider functionality.
9. Provide AI-assisted travel itinerary generation.
10. Provide multilingual assistance.
11. Model Japan-Vietnam remittance.
12. Maintain a tamper-evident audit trail.
13. Demonstrate practical API and security engineering.
14. Provide automated tests for high-risk functionality.

---

## 4. System Architecture

JVCP is divided into a React frontend and Django REST backend.

### Frontend

- React
- Vite
- React Router
- Axios

The frontend provides user-facing interfaces for authentication, identity, providers, marketplace, orders, payments, remittance, itinerary planning, assistant conversations, and administration.

### Backend

The backend is implemented using:

- Django
- Django REST Framework
- PostgreSQL
- Redis
- SimpleJWT
- Google OAuth verification
- Google Gemini / GenAI services

The backend is divided into domain-oriented Django applications:

- `identity`
- `payments`
- `marketplace`
- `providers`
- `itineraries`
- `assistant`
- `remittance`
- `core`

---

## 5. Digital Identity

The identity subsystem provides a reusable user identity profile.

An `IdentityProfile` is associated with a Django user and stores:

- verification status;
- display name;
- country of origin;
- preferred language;
- timestamps.

Supported languages include:

- Vietnamese
- Japanese
- English

The platform also maintains email verification tokens and verification requests.

---

## 6. Email Verification

New accounts are initially inactive.

During registration:

1. A user account is created.
2. The account is marked inactive.
3. A unique email verification token is generated.
4. A verification URL is sent to the user's email.
5. The user opens the verification URL.
6. The account becomes active.
7. The identity profile is marked as verified.
8. JWT access and refresh tokens are returned.

This provides an additional verification step before password-based login is enabled.

---

## 7. Google OAuth

JVCP supports Google login.

The backend receives a Google credential and verifies it using Google's OAuth token verification mechanism and the configured Google client ID.

If the credential is valid, the backend obtains the user's email and creates or retrieves the corresponding account.

JWT access and refresh tokens are then issued by JVCP.

---

## 8. JWT Authentication

Authenticated API operations use JSON Web Tokens.

The frontend stores the access token and attaches it to API requests using:

    Authorization: Bearer <token>

Refresh tokens are also maintained for session continuation.

Authentication is therefore separated from application-domain authorization.

---

## 9. eKYC Prototype

JVCP contains an eKYC-style verification request system.

Supported verification methods include:

- eKYC document scan;
- eKYC selfie/liveness check;
- existing DID/Verifiable Credential import.

Verification requests have lifecycle states including:

- pending;
- under review;
- approved;
- rejected.

The project deliberately uses simulated document references rather than storing real identity documents.

This keeps the prototype architecture realistic without pretending to provide production KYC verification.

---

## 10. DID / Verifiable Credential Prototype

The project models a W3C-style Verifiable Credential architecture.

A credential contains concepts corresponding to:

- issuer;
- subject;
- claims;
- credential identifier;
- issuance time;
- expiration;
- revocation state.

The default issuer is represented by a mock DID:

    did:mock:jvcp-platform

A mock subject DID can be assigned to the verified user.

The credential system supports:

- issuance;
- public verification;
- expiration checking;
- revocation.

### Important limitation

This is not a production DID implementation.

The credential model intentionally represents the structure of a DID/VC system so that it could later be replaced by an actual DID method, credential issuer, wallet, or identity provider.

---

## 11. Public Credential Verification

JVCP exposes a public credential verification endpoint.

A relying party can provide a credential identifier and receive information including:

- validity;
- revocation state;
- expiration state;
- issuer DID;
- subject DID;
- credential claims;
- issuance time;
- expiration time.

This demonstrates the concept of a relying party checking a credential without requiring the relying party to authenticate to JVCP.

---

## 12. Payment Architecture

The payment subsystem models the following lifecycle:

    Order
      ↓
    Payment initiated
      ↓
    Payment confirmed
      ↓
    Order marked paid
      ↓
    Optional refund

Orders belong to authenticated users.

Payment records contain:

- transaction ID;
- payment method;
- payment status;
- initiation timestamp;
- confirmation timestamp.

---

## 13. QR / NFC / Card Payment Prototype

The system supports three payment methods:

- QR code;
- NFC tap;
- mock card.

The QR implementation generates a JVCP payment payload containing:

- transaction identifier;
- amount;
- currency.

The QR payload is explicitly a prototype format.

A real payment deployment would replace this mechanism with a signed payment request compatible with the selected payment provider or payment standard.

NFC and card payment are also simulated rather than connected to real payment networks.

---

## 14. Marketplace and Providers

JVCP contains a provider and marketplace layer for trusted cross-border services.

Providers represent businesses or service providers that can participate in the platform.

The marketplace supports discovery and commerce-oriented interactions.

Provider trust can be represented through verification, ratings and reviews.

The provider architecture is intended to connect identity and commerce rather than treating marketplace listings as anonymous entities.

---

## 15. AI Itinerary Planner

JVCP contains an AI-powered itinerary planning service.

The planner generates structured travel itineraries intended for cross-border travel scenarios.

The generated result is organized around a day-by-day itinerary structure.

The AI component is implemented as an application service so that the model/provider can be replaced independently from the rest of the application.

---

## 16. Multilingual Assistant

The platform contains a conversational assistant designed for Vietnamese, Japanese and English users.

The assistant supports threaded conversations and provides a conversational interface for travel and platform-related assistance.

The implementation separates assistant logic into a service layer so the underlying AI provider can be replaced later.

---

## 17. Remittance

JVCP contains a Japan-Vietnam remittance simulation.

Supported directions are:

- Japan → Vietnam
- Vietnam → Japan

A transfer contains:

- sender;
- recipient name;
- mock recipient account reference;
- direction;
- send amount;
- send currency;
- exchange rate;
- service fee;
- receive amount;
- receive currency;
- transaction identifier;
- transfer status;
- timestamps.

The system therefore models the data and workflow required for a remittance service.

### Important limitation

The recipient account reference is explicitly a mock reference and is never intended to represent a real bank account.

The settlement process is simulated.

A production implementation would integrate with a regulated payment/remittance provider.

---

## 18. Tamper-Evident Audit Trail

JVCP implements a hash-chained audit trail.

Sensitive actions are recorded as `AuditEvent` records.

Events contain:

- actor;
- event type;
- entity type;
- entity ID;
- metadata;
- timestamp;
- previous hash;
- event hash.

Each event's hash is calculated from its own payload and the previous event's hash.

The first event uses a zero-value previous hash.

This creates a sequential integrity chain:

    Event 1
       ↓
    Event 2
       ↓
    Event 3
       ↓
    Event 4

If an event's stored data is modified, recomputation produces a different hash.

The verification service walks through the entire chain and reports the event where the chain becomes invalid.

### Important limitation

This is a tamper-evident audit mechanism, not a blockchain.

There is:

- no distributed consensus;
- no decentralized ledger;
- no independent network of validators.

The database remains the authoritative storage layer.

---

## 19. Security Design

Security was treated as a core engineering requirement.

### 19.1 Login Rate Limiting

The token endpoint is limited to:

    5 requests per minute per IP

This is intended to reduce credential-stuffing and brute-force attempts.

Excessive requests are handled as HTTP 429 responses.

### 19.2 Object-Level Authorization

User-owned resources are queried using the authenticated user as part of the lookup.

For example:

    get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

This prevents a user from accessing another user's order simply by changing an object identifier.

A mismatched owner receives a 404 response.

### 19.3 Authentication

Protected API endpoints require authenticated users through DRF permissions and JWT authentication.

### 19.4 Administrative Operations

Sensitive operations such as credential revocation and audit verification are restricted to administrative users.

### 19.5 Input Validation

Serializer validation is used for API request data including:

- registration;
- passwords;
- payments;
- refunds;
- remittance data;
- identity verification requests.

---

## 20. Data Model

The system uses PostgreSQL as the primary relational database.

Important entities include:

- User
- IdentityProfile
- EmailVerificationToken
- VerificationRequest
- VerifiableCredential
- Provider
- Order
- Payment
- Refund
- RemittanceTransfer
- ExchangeRate
- AnalyticsEvent
- AuditEvent

Relationships are implemented using Django ORM foreign keys and one-to-one relationships.

---

## 21. API Architecture

The backend follows a versioned REST API structure:

    /api/v1/

Major API domains include:

- authentication;
- identity;
- payments;
- marketplace;
- providers;
- itineraries;
- assistant;
- remittance;
- audit.

Example endpoints include:

    POST /api/v1/auth/token/

    POST /api/v1/identity/register/

    GET /api/v1/identity/credentials/<id>/verify/

    POST /api/v1/payments/orders/<id>/pay/

    GET /api/v1/audit/verify/

    POST /api/v1/remittance/quote/

---

## 22. Automated Testing

Automated tests are included for the highest-risk application areas.

The test coverage includes identity, payment and audit functionality.

Important security scenarios include:

- registration validation;
- email verification;
- login throttling;
- credential lifecycle;
- payment lifecycle;
- refund flow;
- object-level authorization;
- audit-chain integrity;
- detection of intentionally corrupted audit records.

The repository also contains test modules for other application domains.

---

## 23. Real vs. Mocked Components

JVCP is explicitly a prototype.

### Implemented application functionality

- Django REST APIs
- PostgreSQL data models
- JWT authentication
- email verification workflow
- Google OAuth verification
- user authorization
- payment state management
- marketplace data structures
- provider functionality
- AI service integration
- remittance data model
- audit-chain implementation

### Simulated / Prototype Components

- DID generation
- Verifiable Credential infrastructure
- eKYC document verification
- eKYC selfie/liveness verification
- QR payment settlement
- NFC payment settlement
- card payment processing
- remittance settlement

These components are intentionally modeled so that real external providers can replace the mock implementations later.

---

## 24. Security and Privacy Risks

A production implementation would need additional controls around:

- storage of government identity documents;
- biometric/selfie information;
- credential key management;
- DID key custody;
- payment credentials;
- financial compliance;
- KYC/AML requirements;
- privacy regulations;
- cross-border data transfers;
- secrets management;
- fraud detection;
- account recovery;
- transaction dispute handling.

The prototype does not claim to solve these production regulatory requirements.

---

## 25. Technical Trade-Offs

### Prototype DID/VC instead of production DID

A mock implementation makes the project easier to demonstrate while preserving the conceptual architecture.

### Simulated payment processing

This avoids handling real financial transactions while still demonstrating payment state transitions, authorization and auditing.

### Database audit chain

A hash chain provides tamper evidence without the operational complexity of blockchain infrastructure.

### Modular services

AI, payment and remittance functionality are separated into services so external providers can be substituted later.

---

## 26. Current Limitations

The main limitations are:

1. DID/VC is a prototype rather than a production decentralized identity system.
2. eKYC checks are simulated.
3. QR/NFC/card payments do not connect to real payment networks.
4. Remittance settlement is simulated.
5. Audit events are stored in a centralized database.
6. Some application domains require additional dedicated test coverage.
7. Production deployment infrastructure still needs to be deployed and validated.

---

## 27. Production Architecture

A production deployment would introduce:

- Gunicorn or another production WSGI/ASGI server;
- Nginx;
- HTTPS/TLS;
- secure secret management;
- production PostgreSQL;
- Redis;
- centralized logging;
- monitoring;
- backups;
- database migration strategy;
- security headers;
- appropriate CORS configuration;
- production domain configuration.

External integrations would include appropriate regulated providers for:

- DID/VC;
- eKYC;
- payments;
- remittance;
- identity verification.

---

## 28. Recommendations

For a production version, the following improvements are recommended:

### Identity

Integrate a standards-compliant DID/VC provider and secure key management.

### eKYC

Use a regulated KYC provider with appropriate document and biometric verification.

### Payments

Integrate a real payment processor supporting Japan and Vietnam and implement signed payment requests.

### Remittance

Integrate a regulated cross-border remittance provider and implement compliance controls.

### Security

Add:

- comprehensive security monitoring;
- fraud detection;
- stronger account recovery;
- secure secrets management;
- penetration testing;
- dependency vulnerability scanning.

### Testing

Expand dedicated automated test coverage to:

- remittance;
- marketplace;
- providers;
- itineraries;
- assistant.

### Deployment

Deploy the production architecture behind HTTPS with Gunicorn and Nginx.

---

## 29. Conclusion

JVCP demonstrates how digital identity, trusted credentials, secure transaction workflows, travel services and cross-border commerce could be combined into a unified Japan-Vietnam digital corridor.

The project focuses not only on feature development but also on:

- security;
- authorization;
- auditability;
- modular architecture;
- API design;
- prototype-to-production separation.

The DID/VC, eKYC, payment and remittance components are intentionally presented as prototypes rather than production financial or identity infrastructure.

This makes JVCP suitable as a technical proof-of-concept demonstrating product engineering decisions, security thinking, API development, and the ability to turn an early-stage cross-border digital-service concept into a working prototype.

**Current limitation:** the rate limiter uses Django's default local-memory cache
(no explicit `CACHES` backend is configured, despite Redis being available in the
stack). This means the rate-limit counter resets on every backend restart and would
not be shared correctly across multiple worker processes in a multi-process
production deployment (e.g. multiple Gunicorn workers), since each process keeps
its own in-memory counter. A production hardening step would be to point
`django-ratelimit` at the existing Redis instance via a proper `CACHES` configuration,
so the limit is enforced consistently across all workers and survives restarts.

## 30. Real-World Issues Found and Fixed During Deployment

Moving from local development to a live AWS deployment surfaced three concrete
issues, each diagnosed and resolved during this project:

### 30.1 Password field rendered as plaintext

The password `<input>` in the login/registration form used a mistyped attribute
(`ttype` instead of `type`), which React silently ignored. The field therefore had
no `type` attribute and defaulted to plain text, meaning every user's password was
visible on screen while typing, in both login and registration modes. Fixed by
correcting the attribute name and verified by confirming the field renders masked
and that the existing "show password" toggle still functions correctly.

### 30.2 CORS origin mismatch silently blocked all authentication

After changing how the frontend was served, every login, registration, and Google
OAuth attempt failed with a generic error. Backend logs showed only CORS preflight
(`OPTIONS`) requests succeeding — the actual `POST` requests never reached Django.
The cause was `CORS_ALLOWED_ORIGINS` in the environment configuration listing an
origin without a port, while the browser was making requests from a different port,
which the browser's CORS policy treats as a distinct, disallowed origin. This
class of failure is easy to misdiagnose as a backend or authentication bug, since
the error surfaced identically across three unrelated auth flows; the actual signal
was in the browser's network tab and the absence of the real request in backend
logs. Fixed by expanding `CORS_ALLOWED_ORIGINS` to include every origin the app is
actually served from.

### 30.3 IDOR — see Section 19.2

Documented separately as a security design decision, since it was caught and fixed
before deployment via a dedicated cross-user test rather than discovered live.

These findings reflect a broader lesson: authorization bugs, UI attribute typos, and
environment-configuration mismatches each produce very different *symptoms* but can
look identical from a user's perspective ("it doesn't work"). Diagnosing each
correctly required checking a different layer of the stack — the React DOM output,
browser network behavior, and server-side request logs, respectively.
