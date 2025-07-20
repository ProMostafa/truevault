# 🔐 TrueIDVault – Secure Identity Vault API

A secure, scalable API for managing encrypted identity records with tiered API key access and rate limiting. Built with Django, Django REST Framework, and PostgreSQL.

---

## 🚀 Features

- 🔐 **API Key-Based Authentication**
- 📊 **Tiered Access Control** (`basic`, `premium`)
- ⚡ **Rate Limiting** (DRF `SimpleRateThrottle` with dynamic per-tier limits)
- 🧪 **Test Coverage** for key components (authentication, validation, throttling)
- 📚 **Validated Egyptian National ID Parser**
- ☁️ **Ready for deployment** (Dockerized, 12-Factor ready)

---

## 🧠 Design Decisions

### ✅ Scalable Rate Limiting by Access Tier

> “I used DRF’s scoped throttling and enforced different rate limits per API key to support tiered access in a real-world SaaS model.”

- Dynamically resolves rate from `APIKey.tier` (`basic`: 5/min, `premium`: 20/min)
- DRF’s `SimpleRateThrottle` overridden to allow custom per-request logic
- Fail-safe fallback to prevent abuse in case of unknown tier

### ✅ Explicit Separation of Concerns

- `throttling.py`: Custom logic for dynamic rate throttling
- `validators.py`: Centralized Egyptian ID validation
- `models.py`: Extensible model for API keys with tier support

### ✅ Developer Experience

- Modular, testable design
- Minimal configuration required for onboarding
- Clear error messages and DRF-friendly exception handling

---

## 🛠️ Setup

```bash
git clone https://github.com/your-org/trueidvault.git
cd trueidvault
python -m venv env
source env/bin/activate
pip install -r requirements.txt
python manage.py migrate
