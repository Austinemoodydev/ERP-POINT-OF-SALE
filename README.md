# poserp

A multi-tenant Point of Sale and ERP platform built with Django. Started this as a side project that grew into something much bigger — it now covers most of what a small-to-medium business would need to run their operations.

Still actively building it. Not production-ready yet but the core is solid.

---

## What it does

At its heart, poserp is a SaaS ERP — multiple businesses (tenants) can use the same installation, each with their own isolated data. It handles everything from ringing up a sale at the counter to generating payroll, tracking inventory across warehouses, managing supplier purchases, and sending automated alerts when stock runs low.

The background job system (Celery) runs nightly tasks automatically — forecasting next month's sales, flagging expiring products, reminding customers about overdue invoices, and emailing scheduled reports to management.

---

## Modules built so far

**Core & SaaS**
- Multi-tenant architecture (each business gets their own subdomain and data)
- Superadmin panel for managing tenants
- User accounts and permissions per tenant

**Point of Sale**
- POS sales interface
- Sales orders, quotations, invoices
- Customer ledger and payment tracking
- Debt reminders via SMS

**Purchasing**
- Supplier management
- Purchase orders
- Goods received tracking

**Inventory**
- Multi-warehouse stock management
- Stock transfers between branches
- Stock adjustments, damaged goods, returns
- Expiry tracking (ProductBatch)
- Cycle counts and stock takes
- Low stock alerts

**Accounting**
- Chart of accounts
- Journal entries
- Payroll journal posting
- Financial reporting

**HR & Payroll**
- Employee management
- Payroll calculation (PAYE included)
- Payslip generation
- Automated payroll processing via background jobs

**CRM**
- Customer relationship management
- Customer profiles linked to sales

**Analytics & Business Intelligence**
- AI-powered sales forecasting
- Forecast snapshots stored in the database
- AI recommendations engine (reorder suggestions, low stock flags)
- KPI tracking with targets vs actuals
- Dashboard widgets (per-user layout)
- Scheduled reports (daily/weekly/monthly via email)

**Compliance**
- Compliance tracking module

**Integrations**
- Email service (Django mail)
- SMS service (Africa's Talking / Twilio — pluggable)
- WhatsApp notifications (WhatsApp Business API — pluggable)
- M-Pesa payment integration
- ERP sync

**Background Processing (Celery)**
- Automated nightly forecasts
- AI recommendation generation
- Low stock alerts
- Expiry alerts (30-day warning)
- Debt reminders
- Payroll automation
- Auto database backups
- Email, SMS, and WhatsApp queues
- Celery Beat scheduler for all of the above

---

## Tech stack

- **Backend** — Django 5.2, Python 3.13
- **Database** — MySQL (via phpMyAdmin locally)
- **Task Queue** — Celery 5.6 + Redis (or SQLite broker for dev)
- **Scheduled Tasks** — django-celery-beat
- **Task Results** — django-celery-results
- **Multi-tenancy** — django-tenants
- **API** — Django REST Framework
- **Frontend** — Django templates (server-rendered)

---

## Project structure

```
poserp/
├── config/          # Settings, URLs, WSGI
├── saas/            # Tenant management
├── core/            # Shared models and utilities
├── sales/           # POS, invoices, orders
├── purchasing/      # Supplier orders
├── inventory/       # Warehouses, stock
├── accounting/      # Ledger, journals
├── hr/              # Employees, payroll
├── crm/             # Customers
├── analytics/       # Forecasting, KPIs, AI
├── integrations/    # Email, SMS, WhatsApp, M-Pesa
├── compliance/      # Regulatory tracking
├── superadminpanel/ # Platform admin
├── api/             # REST endpoints
├── backup/          # Auto backup tasks
├── dashboard/       # Dashboard views
└── celery_app.py    # Celery configuration
```

---

## Getting started

**Requirements**
- Python 3.13
- MySQL
- Redis (or Memurai on Windows)

**Setup**

```bash
# Clone the repo
git clone https://github.com/yourusername/poserp.git
cd poserp

# Install dependencies
pip install -r requirements.txt

# Set up the database
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Run the dev server
python manage.py runserver
```

**Running background tasks**

```bash
# Terminal 1 — Celery worker
celery -A celery_app worker -l info --pool=solo

# Terminal 2 — Celery Beat scheduler
celery -A celery_app beat -l info
```

> On Windows use `--pool=solo` to avoid multiprocessing issues.

---

## Current status

Most of the core modules are built and migrating cleanly. Actively working through:

- Stabilizing all Celery tasks
- Wiring up the remaining integrations (SMS, WhatsApp)
- Building out the dashboard views
- API endpoints for mobile/frontend use

This is a solo build — started from scratch and building each module one phase at a time. The goal is a full enterprise ERP that small businesses in Kenya (and elsewhere) can actually afford to use.

---

## Roadmap (next phases)

- [ ] Workflow & approval chains (BPM engine)
- [ ] Document management
- [ ] Electronic signatures
- [ ] Mobile app (React Native or Flutter)
- [ ] Executive dashboard with real-time KPIs
- [ ] Predictive cash flow analysis
- [ ] Multi-currency support
- [ ] WhatsApp Business API full integration
- [ ] Africa's Talking SMS full integration

---

## Contributing

Not open for contributions yet — still in active solo development. Will update this when the codebase stabilizes.

---

## License

Private project. Will decide on licensing once it's closer to release.

---

*Built in Nairobi. Figuring it out one error at a time.*
