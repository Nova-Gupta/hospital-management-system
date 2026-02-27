# 🏥 Hospital Management System

A scalable, production-ready full-stack application built with **Django REST Framework** on the backend and a **fully responsive HTML/CSS/JS frontend**. It manages hospital operations including doctor and patient management, appointment scheduling, prescriptions, and billing — with JWT authentication, role-based access control, Redis caching, and deployment on Render.

> 🌐 **Live Demo:** [https://hospital-management-system-y46v.onrender.com/static/login.html](https://hospital-management-system-y46v.onrender.com/static/login.html)

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Technology Stack](#technology-stack)
- [Features](#features)
- [Project Structure](#project-structure)
- [Database Design](#database-design)
- [API Endpoints](#api-endpoints)
- [Frontend](#frontend)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [Running with Docker](#running-with-docker)
- [Deployment](#deployment)
- [Security](#security)
- [Performance Optimizations](#performance-optimizations)
- [Future Scope](#future-scope)

---

## 📌 Project Overview

The Hospital Management System provides a complete platform for managing hospital workflows. The Django REST API powers three role-based portals — Admin, Doctor, and Patient — all accessible through a responsive web frontend that works seamlessly on mobile, tablet, and desktop.

---

## 🛠 Technology Stack

| Layer | Technology |
|---|---|
| Backend | Django 4.2, Django REST Framework |
| Database | PostgreSQL 15 |
| Cache | Redis 7 |
| Authentication | JWT (djangorestframework-simplejwt) |
| Server | Gunicorn (3 workers) |
| Static Files | Whitenoise |
| Frontend | HTML5, CSS3, Vanilla JavaScript (self-contained) |
| Containerization | Docker, Docker Compose |
| Deployment | Render |

---

## ✨ Features

### Backend
- JWT authentication with token blacklisting on logout
- Role-based access control — Admin, Doctor, Patient
- Auto-creation of Doctor/Patient profiles via Django signals
- Double-booking prevention on appointments
- JSON-based prescription medication records
- Invoice auto-calculation (amount + tax − discount)
- Redis-cached dashboard analytics (5-minute TTL)
- Django admin panel for full data management

### Frontend
- **Fully responsive** — works on mobile, tablet, and desktop
- **Self-contained HTML files** — no external CSS dependencies
- Mobile sidebar with hamburger toggle (☰)
- Role-based auto-redirect after login
- Toast notifications for all actions
- Loading states and empty state displays
- Horizontal table scroll on small screens

### Security
- Admin accounts cannot be registered via the public API or frontend
- All API secrets and credentials via environment variables
- HTTPS enforced on Render
- Password hashing via Django's PBKDF2 + SHA256

---

## 📁 Project Structure

```
hospital-management-system/
├── Dockerfile
├── docker-compose.yml
├── render.yaml
├── requirements.txt
├── manage.py
├── .env
├── .env.example
├── .gitignore
├── README.md
│
├── frontend/                        ← Responsive web frontend
│   ├── login.html                   ← Two-column desktop, single-column mobile
│   ├── register.html                ← Doctor/Patient registration only
│   ├── admin_dashboard.html         ← Admin portal
│   ├── doctor_dashboard.html        ← Doctor portal
│   ├── patient_dashboard.html       ← Patient portal
│   └── shared.css                   ← Base styles (legacy, dashboards self-contained)
│
└── hospital/
    ├── settings.py
    ├── urls.py
    ├── wsgi.py
    └── apps/
        ├── accounts/                ← Custom User model, JWT auth, signals
        ├── doctors/                 ← Doctor profiles
        ├── patients/                ← Patient profiles
        ├── appointments/            ← Appointment booking
        ├── prescriptions/           ← Prescription records
        ├── billing/                 ← Invoicing and payments
        └── dashboard/               ← Analytics with Redis caching
```

---

## 🗄 Database Design

```
User (Custom AbstractUser)
 ├── role: admin | doctor | patient
 ├── phone
 │
 ├── Doctor (OneToOne → User)
 │    ├── specialization, license_number
 │    ├── experience_years, consultation_fee
 │    └── is_available
 │
 └── Patient (OneToOne → User)
      ├── date_of_birth, blood_group
      ├── address, emergency_contact
      └── medical_history

Appointment (ForeignKey → Doctor, Patient)
 ├── appointment_date + appointment_time  ← unique together per doctor
 ├── status: pending | confirmed | completed | cancelled
 └── reason, notes

Prescription (OneToOne → Appointment)
 ├── diagnosis
 ├── medications: JSONField [{name, dosage, frequency, duration}]
 └── instructions, follow_up_date

Invoice (OneToOne → Appointment)
 ├── amount, tax, discount
 ├── total_amount  ← auto-calculated on save
 ├── payment_status: pending | paid | cancelled
 └── payment_method: cash | card | online | insurance
```

---

## 🔗 API Endpoints

### Auth
| Method | Endpoint | Access | Description |
|---|---|---|---|
| POST | `/api/auth/register/` | Public | Register as doctor or patient only |
| POST | `/api/auth/login/` | Public | Login, receive JWT tokens |
| POST | `/api/auth/refresh/` | Public | Refresh access token |
| GET | `/api/auth/register/profile/` | Authenticated | Get current user profile |
| POST | `/api/auth/register/logout/` | Authenticated | Logout and blacklist token |

### Doctors
| Method | Endpoint | Access | Description |
|---|---|---|---|
| GET | `/api/doctors/` | Any | List all doctors |
| GET | `/api/doctors/me/` | Doctor | Get own profile |
| PUT | `/api/doctors/me/` | Doctor | Update own profile |
| GET | `/api/doctors/available/` | Any | List available doctors |

### Patients
| Method | Endpoint | Access | Description |
|---|---|---|---|
| GET | `/api/patients/` | Admin / Doctor | List all patients |
| GET | `/api/patients/me/` | Patient | Get own profile |
| PUT | `/api/patients/me/` | Patient | Update own profile |

### Appointments
| Method | Endpoint | Access | Description |
|---|---|---|---|
| POST | `/api/appointments/` | Patient | Book an appointment |
| GET | `/api/appointments/` | Any | List own appointments (role-filtered) |
| PATCH | `/api/appointments/{id}/update_status/` | Doctor / Admin | Update status |

### Prescriptions
| Method | Endpoint | Access | Description |
|---|---|---|---|
| POST | `/api/prescriptions/` | Doctor / Admin | Create prescription |
| GET | `/api/prescriptions/` | Any | List own prescriptions (role-filtered) |

### Billing
| Method | Endpoint | Access | Description |
|---|---|---|---|
| POST | `/api/billing/` | Admin | Create invoice |
| GET | `/api/billing/` | Any | List own invoices (role-filtered) |
| PATCH | `/api/billing/{id}/mark_paid/` | Admin | Mark invoice as paid |

### Dashboard
| Method | Endpoint | Access | Description |
|---|---|---|---|
| GET | `/api/dashboard/` | Admin | System analytics (Redis cached, 5 min TTL) |

---

## 🖥 Frontend

The frontend is a set of **fully self-contained HTML files** served via Django's static files (Whitenoise). Every file has all CSS embedded inline — no external stylesheet dependencies.

### Pages

| Page | URL | Description |
|---|---|---|
| Login | `/static/login.html` | Two-column on desktop, single-column on mobile |
| Register | `/static/register.html` | Doctor or Patient only |
| Admin Dashboard | `/static/admin_dashboard.html` | Stats, doctors, patients, appointments, billing |
| Doctor Dashboard | `/static/doctor_dashboard.html` | Appointments, prescriptions, profile |
| Patient Dashboard | `/static/patient_dashboard.html` | Book appointments, prescriptions, billing |

### Responsive Behaviour

| Screen | Behaviour |
|---|---|
| Mobile (< 768px) | Sidebar hidden, hamburger ☰ toggles it, stats 2-column, tables scroll |
| Tablet (768px–1100px) | Sidebar visible, two-column sections collapse to one |
| Desktop (> 1100px) | Full layout with sidebar, 3–4 column stats grid |

### Authentication Flow

```
Login → JWT stored in localStorage
      → GET /api/auth/register/profile/
      → role === 'admin'   → admin_dashboard.html
      → role === 'doctor'  → doctor_dashboard.html
      → role === 'patient' → patient_dashboard.html
```

### Security

- Admin role **removed** from registration dropdown
- Backend **rejects** any API attempt to register with `role: admin`
- Admins can only be created by a superuser via the Django admin panel at `/admin/`

---

## 🚀 Getting Started

### Prerequisites

- [Docker](https://www.docker.com/get-started) and Docker Compose
- [Git](https://git-scm.com/)

### Clone and Run

```bash
git clone https://github.com/YOUR_USERNAME/hospital-management-system.git
cd hospital-management-system

# Create your env file
cp .env.example .env
# Edit .env with your values

# Build and start all services
docker-compose up --build
```

Visit: **http://localhost:8000/static/login.html**

---

## ⚙️ Environment Variables

Create a `.env` file in the project root:

```env
# Django
SECRET_KEY=your-super-secret-key-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=hospital_db
DB_USER=postgres
DB_PASSWORD=hospital_pass
DB_HOST=db
DB_PORT=5432

# Redis
REDIS_URL=redis://redis:6379/1

# Auto-created superuser on deploy
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@hospital.com
DJANGO_SUPERUSER_PASSWORD=YourStrongPassword@123
```

---

## 🐳 Running with Docker

```bash
# Start all containers (web, PostgreSQL, Redis)
docker-compose up --build

# Run in background
docker-compose up --build -d

# Stop containers
docker-compose down

# Stop and wipe all data (fresh start)
docker-compose down -v
```

### Services started

| Service | Port | Description |
|---|---|---|
| web | 8000 | Django + Gunicorn |
| db | 5432 | PostgreSQL 15 |
| redis | 6379 | Redis 7 |

---

## ☁️ Deployment

Deployed on **Render** using `render.yaml` blueprint.

### Live URLs

```
Frontend  →  https://hospital-management-system-y46v.onrender.com/static/login.html
API       →  https://hospital-management-system-y46v.onrender.com/api/
Admin     →  https://hospital-management-system-y46v.onrender.com/admin/
```

### Deploy your own

1. Push your code to GitHub
2. Go to [render.com](https://render.com) → **New → Blueprint**
3. Connect your GitHub repository
4. Render auto-detects `render.yaml` and provisions the web service, PostgreSQL, and Redis
5. Add environment variables in the Render dashboard
6. Deploy — Render runs `migrate`, `collectstatic`, and starts Gunicorn automatically

---

## 🔒 Security

| Measure | Implementation |
|---|---|
| Authentication | JWT with token blacklisting on logout |
| Admin registration | Blocked at both frontend and API level |
| Role enforcement | Permission classes on every endpoint |
| Secrets | All credentials via environment variables |
| HTTPS | Enforced by Render in production |
| Password hashing | Django PBKDF2 + SHA256 |
| Production flags | `DEBUG=False`, `SECURE_SSL_REDIRECT=False` (Render handles SSL) |

---

## ⚡ Performance Optimizations

| Optimization | Detail |
|---|---|
| Redis caching | Dashboard stats cached for 5 minutes |
| `select_related()` | Applied on all ViewSets to prevent N+1 queries |
| Aggregation | Revenue totals use Django `Sum()` |
| Pagination | All list endpoints return 10 items per page |
| Gunicorn workers | 3 workers for concurrent request handling |
| Whitenoise | Compressed static file serving with long-lived cache headers |

---

## 🔮 Future Scope

- **Celery + Redis** — async email notifications on appointment booking/confirmation
- **React / Next.js frontend** — full SPA connecting to the existing API
- **Load balancing** — multiple Gunicorn instances behind a reverse proxy
- **Read replicas** — separate read/write database connections for scale
- **Mobile app** — React Native app using the same REST API

---

## 👨‍💻 Author

Built with ❤️ using Django REST Framework, PostgreSQL, Redis, Docker, and Vanilla JS.