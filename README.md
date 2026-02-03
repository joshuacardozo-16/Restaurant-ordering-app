# Restaurant-ordering-app

🍽️ Saffron & Smoke — Cloud Restaurant Ordering Platform

A full-stack, production-ready restaurant ordering system built with Flask, designed using hybrid cloud architecture that combines:

✅ SQL relational data (PostgreSQL)
✅ NoSQL analytics (Google Firestore)
✅ Cloud-native deployment (Google App Engine)

This system allows customers to browse a menu, place delivery or pickup orders, earn loyalty rewards, and receive automated confirmation emails — while administrators gain real-time business insights through analytics dashboards.


Live Deployment

👉 Production URL:

https://saffron-smoke-personal.nw.r.appspot.com

Hosted fully on Google Cloud Platform using App Engine.


Architecture Overview

Client Browser
     ↓
Google App Engine (Flask + Gunicorn)
     ↓
-----------------------------
|           |               |
Cloud SQL   Firestore      Cloud Run
(Postgres)  (NoSQL)        (Email Service)


            Tech Stack
Backend
- Python 3.11
- Flask
- SQLAlchemy
- Gunicorn


Databases
✅ SQL (Primary)

Google Cloud SQL — PostgreSQL

Stores:
- Users
- Orders
- Menu items
- Loyalty accounts
- Transactions

✅ NoSQL (Analytics)
Google Firestore

Used for event-driven analytics:
- menu_view
- add_to_cart
- checkout_view
- order_placed

Enables admin dashboards such as:
- Conversion funnel
- Popular items
- Customer behaviour
- Peak ordering hours

Cloud Services
- Google App Engine (deployment)
- Cloud SQL (managed PostgreSQL)
- Firestore (NoSQL analytics)
- Cloud Run (order confirmation emails)
- Google Maps API (delivery distance + ETA)
- SendGrid (email delivery)

✨ Core Features

👤 Customer Features
✅ Secure registration & login
✅ Browse categorized menu
✅ Add/remove items from cart
✅ Delivery OR Pickup

🧮 Smart Pricing
- 15% discount for pickup
- 10% discount for new customers

🚚 Delivery Intelligence
- Powered by Google Maps API:
- Distance calculation
- Delivery eligibility
- ETA estimation

🎁 Loyalty Rewards System
Customers earn points automatically and can:
✅ Redeem rewards
✅ Apply discounts
✅ Track balances

📦 Order Management
Customers can:
- View order history
- Track statuses

🛠️ Admin Features
Dashboard Analytics
Using Firestore event data:
✅ Revenue metrics
✅ Total orders
✅ Conversion funnel
✅ Popular items
✅ Peak hours

Menu Management
Admins can:
- Create items
- Update availability
- Manage categories

Order Control
Admins can update status:
- Preparing
- Delivered
- Cancelled

Automated Testing
This project uses pytest for backend testing.
Run Tests
From the project root:
 - python -m pytest -q

 - Test Coverage Includes
✅ Authentication
✅ Admin APIs
✅ Cart logic
✅ Checkout flow
✅ Delivery quotes
✅ Email service
✅ Menu endpoints
✅ Order APIs

💻 Running Locally
Create Virtual Environment

Install Dependencies
pip install -r requirements.txt

Windows 
.\venv\Scripts\Activate.ps1
.\env.ps1
python run.py   


🗄️ Database Evolution (IMPORTANT FOR MARKERS)
Phase 1 — Local Development
Initially built using:

👉 SQLite

Allowed rapid prototyping without cloud costs.

Phase 2 — Production Migration
Migrated to:

👉 Google Cloud SQL (PostgreSQL)

Benefits:

scalability

reliability

managed backups

production-grade performance

This demonstrates real-world deployment skills.

🔐 Security Notes
The following files are intentionally excluded from Git:

app.yaml
env.ps1
*.json

These contain:
- API keys
- database credentials
- service account secrets
This follows industry security practices.




Deployment Guide (High Level)

Deploy using:
- gcloud app deploy


View logs:
- gcloud app logs tail -s default


Open app:
- gcloud app browse


Future Improvements

Suggested production upgrades:
- Docker containerization
- CI/CD pipeline
- Redis caching
- Stripe payments
- Async workers (Celery)
- Terraform infrastructure