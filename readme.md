# 🔐 TrueVault – Secure Identity Vault API

TrueVault is A secure, scalable API service in Python to validate and extract information from an Egyptian national ID number. Built with Django, Django REST Framework, and PostgreSQL.

---

## Features

- **Validated Egyptian National ID Parser**
- **API Key-Based Authentication**
- **Tiered Access Control** (`basic`, `premium`)
- **Rate Limiting** (DRF `SimpleRateThrottle` with dynamic per-tier limits)
- **Test Coverage** for key components (authentication, validation, throttling)
- **Ready for deployment** (Dockerized)

---

## Architecture Consideration
- Secure user data
- Validate & Extract information from National ID
- Audit Logging & Tracking
- Modular, Separation of Concerns that easy support Adding new features
- High performance
- APK-Key service to service commnuicates
- Design database models that can support incoming subscriptions model & future reports (Assumption)
- Permissions strategy that can enable APK can access which service (Assumption in futute can Add mor Services)
- Rate Limiting by Access Tier


### How TrueVault Achieve this Considerations
## ✅ Secure User Data
- Use HTTPS protocol and POST method to:
  - Encrypt data in transit
  - Protect sensitive data from interception
- In production:
  - Consider encrypting data at rest using strong encryption (e.g., AES-256)

## 🆔 Validate & Extract Information from Egyptian National ID
- Follow the official Egyptian National ID structure
- Extract data according to government rules:
  - Birthdate
  - Gender
  - Governorate
- Handle invalid structures by validating:
  - Format (must be 14 digits)
  - Logical correctness (e.g., valid dates, governor codes)

## 📜 Audit Logging & Tracking
- Log each API call with:
  - `api_key`
  - `endpoint`
  - `request_data_hash`
  - `response_status`
  - `timestamp`
- Use asynchronous logging to avoid blocking under high load

## 🧱 Modular Architecture with Separation of Concerns
- Follow Django best practices and SOLID principles
- Design small, reusable apps with single responsibility
- Easy to extend, test, and maintain

## ⚡ High Performance
- Implement async logging to reduce latency under high load
- (Optional) Caching for repeated validations and static lookups (e.g., Redis)

## 🔑 API Key-Based Service-to-Service Authentication
- Implement strong SHA-256 API keys
- Each API key includes:
  - `is_active`: Whether the key is currently valid
  - `expires_at`: Optional expiry date
  - `tier`: Access level (e.g., free, premium)

## 🧮 Database Models for Subscription Support & Future Reports
- Designed with extensibility in mind, assuming future billing or service tracking needs

### UML Diagram (Text-Based)
```
+----------------------+
|      Service         |
+----------------------+
| - name: CharField    |
| - description: Text  |
+----------------------+
| + is_authenticated() |
| + __str__()          |
+----------------------+
           ▲
           |
           | 1
           |
           | *
+----------------------+
|       APIKey         |
+----------------------+
| - key: CharField     |
| - tier: CharField    |
| - is_active: Boolean |
| - expires_at: Date   |
| - created_at: Date   |
+----------------------+
| + __str__()          |
| * permissions        |
| FK: service_id       |
+----------------------+

+------------------------------+
|     ServicePermission        |
+------------------------------+
| - code: CharField            |
| - description: TextField     |
+------------------------------+
| + __str__()                  |
+------------------------------+
```

## 🧩 Permission Strategy per API Key
- Each API key is granted permission for specific services
- Prevents opening all services to all clients
- Enables fine-grained access control
- Supports future expansion to more services/modules

## 🚦 Rate Limiting by Access Tier
- API key tier controls:
  - Quota limits (e.g., 5 requests/min for free, 100 for premium)
- Helps prevent abuse and ensures fair usage
- Implemented using:
  - Django REST Framework’s throttling system
  - Custom throttle classes or third-party packages (e.g., django-ratelimit)


### Go to [Installation Guide ](https://github.com/ProMostafa/truevault/blob/master/installation_guide.md)