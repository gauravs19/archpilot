# Security Architecture Standards

> **Purpose:** This rule file defines enterprise security architecture standards covering
> authentication, authorization, encryption, threat modeling, and compliance. When used as
> LLM context, it ensures every design incorporates security as a first-class concern.

---

## How to Use This File

- **Claude Projects:** Upload for security architecture reviews and threat modeling
- **Design Reviews:** Use the checklists to audit designs for security gaps
- **Any LLM:** Say: *"Using these security standards, review this design for vulnerabilities: [paste design]"*

---

## Related Standards

| Standard | Relationship |
|----------|-------------|
| [00 — Architecture Principles](./00-architecture-principles.md) | Security Principles (§5) expanded here |
| [05 — API Design](./05-api-design.md) | API security, auth headers, rate limiting |
| [06 — Data Architecture](./06-data-architecture.md) | Data classification, PII handling, encryption |
| [12 — Observability](./12-observability-standards.md) | Security event logging and audit trails |
| [11 — NFR Checklist](./11-nfr-checklist.md) | Security section of the NFR audit |

---

## 1. Core Security Principles

### 1.1 Zero Trust
- **Never trust, always verify.** Every request is authenticated and authorized, regardless of network location.
- No implicit trust based on IP address, VPN, or network segment.
- Every service-to-service call MUST be authenticated (mTLS, JWT, or service tokens).

### 1.2 Defense in Depth
Security controls must exist at EVERY layer:

```
[WAF / CDN] → [API Gateway] → [Service Mesh / mTLS] → [Application] → [Database]
    ↑              ↑                    ↑                    ↑             ↑
  DDoS          Rate Limit          AuthN/AuthZ          Input         Encryption
  Protection    CORS                Token Verify         Validation   at Rest
  Bot Detection Request Validation  RBAC/ABAC            Sanitization Row-Level Security
```

### 1.3 Least Privilege
- Every user, service, and process operates with the MINIMUM permissions required.
- Database connections use role-specific accounts (not root/admin).
- Service accounts have scoped permissions (not wildcard `*`).
- Temporary elevated access via just-in-time (JIT) provisioning.

### 1.4 Secure by Default
- All new services start with most restrictive configuration.
- New API endpoints are authenticated by default; public access requires explicit opt-in.
- Default to deny; explicitly grant permissions.

---

## 2. Authentication Standards

### 2.1 User Authentication

| Pattern | When to Use | Implementation |
|---------|------------|----------------|
| **OAuth 2.0 + OIDC** | Web/mobile apps with user login | Authorization Code flow with PKCE |
| **JWT Access Tokens** | API authentication for logged-in users | Short-lived (15 min), signed with RS256 |
| **Refresh Tokens** | Token renewal without re-login | Long-lived (7 days), stored securely, rotated on use |
| **Session-Based** | Traditional web apps | Server-side sessions with secure, httpOnly cookies |
| **Passkeys / WebAuthn** | Passwordless authentication | Preferred for new applications |

**JWT Rules:**
- Access tokens MUST expire within 15-30 minutes.
- Use RS256 (asymmetric) for tokens verified by multiple services.
- Use HS256 (symmetric) only when a single service issues AND verifies.
- NEVER store sensitive data in JWT payload (it's base64, not encrypted).
- Token MUST include: `sub` (user ID), `iss` (issuer), `exp` (expiry), `iat` (issued at), `roles`.
- Validate ALL claims: `iss`, `aud`, `exp`, `nbf`. Do not skip validation.

### 2.2 Service-to-Service Authentication

| Pattern | When to Use |
|---------|------------|
| **mTLS (Mutual TLS)** | Service mesh environments (Istio, Linkerd) |
| **Service Tokens (JWT)** | API-to-API calls with centralized identity provider |
| **API Keys** | Third-party integrations, webhook callbacks |
| **IAM Roles** | Cloud-native service auth (AWS IAM, GCP Service Accounts) |

**Rules:**
- API Keys MUST be rotated every 90 days.
- API Keys MUST NOT be embedded in source code.
- Service tokens MUST be short-lived and auto-refreshed.

### 2.3 Multi-Factor Authentication (MFA)
- MFA MUST be enforced for: admin access, production system access, CI/CD pipeline approval.
- MFA SHOULD be available for all user accounts.
- TOTP (Google Authenticator) or hardware keys (YubiKey) preferred over SMS.

---

## 3. Authorization Standards

### 3.1 RBAC (Role-Based Access Control)

Define roles at the application level:

| Role | Permissions | Example |
|------|-----------|---------|
| `viewer` | Read-only access | Dashboard viewing |
| `editor` | Read + Write | Content management |
| `admin` | Full access to single tenant | Tenant administration |
| `super_admin` | Cross-tenant, system-level access | Platform operations |
| `service` | Machine-to-machine | Microservice calls |

**Rules:**
- Roles MUST be assigned to users, not hardcoded in code.
- Permission checks MUST happen at the API layer, not the UI layer.
- Admin roles SHOULD require MFA.
- Role assignments MUST be auditable (who granted what, when).

### 3.2 ABAC (Attribute-Based Access Control)
For fine-grained access (when RBAC is too coarse):
- Evaluate based on: user attributes (role, department), resource attributes (owner, classification), action, context (time, IP, device).
- Use for: multi-tenant data isolation, document ownership, geographic restrictions.

### 3.3 Authorization at Every Layer

| Layer | Check |
|-------|-------|
| **API Gateway** | Valid token, rate limits, IP allowlist |
| **Service** | Role-based endpoint access, business rule authorization |
| **Database** | Row-level security, column-level masking |
| **File Storage** | Pre-signed URLs with expiration, bucket policies |

---

## 4. Data Protection

### 4.1 Encryption at Rest

| Data Store | Encryption | Key Management |
|-----------|-----------|----------------|
| Database | AES-256 (TDE or column-level) | Cloud KMS (AWS KMS, Azure Key Vault) |
| Object Storage | SSE-S3/SSE-KMS | Customer-managed keys preferred |
| Cache (Redis) | At-rest encryption enabled | Managed service encryption |
| Backups | Encrypted with separate key | Key rotation every 12 months |
| Logs | Encrypted at rest | PII MUST be redacted before logging |

### 4.2 Encryption in Transit
- ALL communication MUST use TLS 1.2+ (TLS 1.3 preferred).
- Internal service-to-service traffic MUST be encrypted (mTLS or TLS).
- Certificate management via automated renewal (Let's Encrypt, ACM, cert-manager).
- HSTS headers MUST be set with `max-age >= 31536000` (1 year).

### 4.3 PII Handling

| Practice | Rule |
|----------|------|
| **Identification** | All PII fields MUST be tagged in data models |
| **Minimization** | Collect only PII that is strictly necessary |
| **Masking** | PII MUST be masked in logs, error messages, and non-production environments |
| **Retention** | PII MUST have a defined retention period with automated deletion |
| **Access Logging** | All access to PII MUST be logged for audit |
| **Right to Deletion** | Systems MUST support data deletion requests (GDPR Article 17) |

### 4.4 Secrets Management

| ❌ NEVER | ✅ ALWAYS |
|----------|----------|
| Secrets in source code | Use secrets manager (AWS SM, Vault, Azure KV) |
| Secrets in environment variables (plain text) | Inject at runtime from secrets manager |
| Secrets in config files | Reference secrets by ID, not value |
| Same secret across environments | Unique secrets per environment |
| Long-lived secrets | Rotate every 90 days minimum |
| Shared credentials | Per-service, per-environment credentials |

---

## 5. Threat Modeling (STRIDE)

For every new system or feature, assess threats using STRIDE:

| Threat | Question | Mitigation |
|--------|----------|-----------|
| **S**poofing | Can an attacker pretend to be someone else? | Strong authentication, MFA |
| **T**ampering | Can data be modified in transit or at rest? | Encryption, integrity checks, signing |
| **R**epudiation | Can a user deny performing an action? | Audit logging, non-repudiation tokens |
| **I**nformation Disclosure | Can unauthorized parties access sensitive data? | Encryption, access control, data classification |
| **D**enial of Service | Can the system be overwhelmed? | Rate limiting, auto-scaling, DDos protection |
| **E**levation of Privilege | Can a user gain unauthorized access? | Least privilege, input validation, RBAC |

---

## 6. Network Security

### 6.1 Network Architecture

```
                    ┌─────────────────────────────┐
                    │         WAF / CDN            │
                    └──────────┬──────────────────┘
                               │
                    ┌──────────▼──────────────────┐
                    │    Public Subnet             │
                    │    (Load Balancer, API GW)    │
                    └──────────┬──────────────────┘
                               │
                    ┌──────────▼──────────────────┐
                    │    Private Subnet            │
                    │    (Application Services)     │
                    └──────────┬──────────────────┘
                               │
                    ┌──────────▼──────────────────┐
                    │    Data Subnet               │
                    │    (Databases, Caches)        │
                    └─────────────────────────────┘
```

**Rules:**
- Databases MUST NOT be publicly accessible.
- Application services SHOULD be in private subnets.
- Security groups follow least-privilege (no `0.0.0.0/0` ingress except LB).
- VPC flow logs MUST be enabled for network monitoring.

---

## 7. Application Security Checklist

### OWASP Top 10 Coverage

| # | Risk | Standard Mitigation |
|---|------|-------------------|
| A01 | Broken Access Control | RBAC at every layer, deny by default |
| A02 | Cryptographic Failures | TLS everywhere, AES-256, no MD5/SHA1 |
| A03 | Injection (SQL, NoSQL, OS) | Parameterized queries, ORM, input validation |
| A04 | Insecure Design | Threat modeling, secure design patterns |
| A05 | Security Misconfiguration | Hardened defaults, automated config scanning |
| A06 | Vulnerable Components | Dependency scanning (Snyk, Dependabot), automated patching |
| A07 | Auth & Identity Failures | MFA, secure token handling, account lockout |
| A08 | Software & Data Integrity | Code signing, SBOM, supply chain verification |
| A09 | Logging & Monitoring Failures | Security event logging, SIEM integration, alerting |
| A10 | SSRF | URL validation, allowlists, network segmentation |

---

## 8. Compliance Matrix

| Requirement | GDPR | SOC2 | PCI-DSS | HIPAA |
|------------|:----:|:----:|:-------:|:-----:|
| Data encryption at rest | ✅ | ✅ | ✅ | ✅ |
| Data encryption in transit | ✅ | ✅ | ✅ | ✅ |
| Access control / RBAC | ✅ | ✅ | ✅ | ✅ |
| Audit logging | ✅ | ✅ | ✅ | ✅ |
| Data retention policy | ✅ | ✅ | ✅ | ✅ |
| Right to deletion | ✅ | | | |
| Data residency / sovereignty | ✅ | | | |
| Vulnerability scanning | | ✅ | ✅ | ✅ |
| Penetration testing | | ✅ | ✅ | ✅ |
| Incident response plan | ✅ | ✅ | ✅ | ✅ |
| Business continuity plan | | ✅ | ✅ | ✅ |

---

*Archpilot — Enterprise Architecture Standards Library*
*Created by Gaurav Sharma*
