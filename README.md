# 🏥 Hospital Management System

A scalable, production-ready backend REST API built with **Django** and **Django REST Framework**, featuring role-based authentication, appointment booking, prescriptions, billing, Redis caching, a responsive web frontend, and full Docker + Render deployment.

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

The Hospital Management System is a full-stack application with a Django REST API backend and a responsive HTML/CSS/JS frontend. It manages hospital operations including doctor and patient management, appointment scheduling, prescriptions, and billing. It implements JWT-based authentication with role-based access control for three user types: **Admin**, **Doctor**, and **Patient**.

---

## 🛠 Technology Stack

| Layer | Technology |
|---|---|
| Backend | Django 4.2, Django REST Framework |
| Database | PostgreSQL 15 |
| Cache | Redis 7 |
| Authentication | JWT (djangorestframework-simplejwt) |
| Server | Gunicorn |
| Static Files | Whitenoise |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Containerization | Docker, Docker Compose |
| Deployment | Render |

---

## ✨ Features

- **JWT Authentication** — Secure login, token refresh, and token blacklisting on logout
- **Role-Based Access Control** — Three roles: Admin, Doctor, Patient with scoped permissions
- **Secure Registration** — Admin accounts can only be created via Django admin panel, not via API
- **Doctor Management** — Profile management, specialization, availability, consultation fee
- **Patient Management** — Profile management, medical history, blood group
- **Appointment Booking** — Book appointments with double-booking prevention
- **Prescription Module** — JSON-based medication records linked to appointments
- **Billing & Invoicing** — Invoice creation, payment tracking, mark-as-paid functionality
- **Dashboard Analytics** — Aggregated stats with Redis caching (5-minute TTL)
- **Auto Profile Creation** — Doctor/Patient profiles auto-created via Django signals on registration
- **Responsive Frontend** — Mobile-friendly dashboards for Admin, Doctor, and Patient
- **Admin Panel** — Full Django admin interface for all models

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
├── .gitignore
├── README.md
├── frontend/                    ← Responsive web frontend
│   ├── login.html
│   ├── register.html
│   ├── admin_dashboard.html
│   ├── doctor_dashboard.html
│   ├── patient_dashboard.html
│   └── shared.css
└── hospital/
    ├── settings.py
    ├── urls.py
    ├── wsgi.py
    └── apps/
        ├── accounts/        # Custom User model, JWT auth, signals
        ├── doctors/         # Doctor profiles and management
        ├── patients/        # Patient profiles and management
        ├── appointments/    # Appointment booking system
        ├── prescriptions/   # Prescription records
        ├── billing/         # Invoice and payment tracking
        └── dashboard/       # Analytics with Redis caching
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
 ├── appointment_date + appointment_time (unique together per doctor)
 ├── status: pending | confirmed | completed | cancelled
 └── reason, notes

Prescription (OneToOne → Appointment)
 ├── diagnosis
 ├── medications (JSONField: [{name, dosage, frequency, duration}])
 └── instructions, follow_up_date

Invoice (OneToOne → Appointment)
 ├── amount, tax, discount, total_amount (auto-calculated)
 ├── payment_status: pending | paid | cancelled
 └── payment_method: cash | card | online | insurance
```

---

## 🔗 API Endpoints

### Auth
| Method | Endpoint | Access | Description |
|---|---|---|---|
| POST | `/api/auth/register/` | Public | Register as doctor or patient only |
| POST | `/api/auth/login/` | Public | Login, get JWT tokens |
| POST | `/api/auth/refresh/` | Public | Refresh access token |
| GET | `/api/auth/register/profile/` | Any | Get current user profile |
| POST | `/api/auth/register/logout/` | Any | Logout, blacklist token |

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
| GET | `/api/patients/` | Admin/Doctor | List all patients |
| GET | `/api/patients/me/` | Patient | Get own profile |
| PUT | `/api/patients/me/` | Patient | Update own profile |

### Appointments
| Method | Endpoint | Access | Description |
|---|---|---|---|
| POST | `/api/appointments/` | Patient | Book appointment |
| GET | `/api/appointments/` | Any | List own appointments (role-filtered) |
| PATCH | `/api/appointments/{id}/update_status/` | Doctor/Admin | Update status |

### Prescriptions
| Method | Endpoint | Access | Description |
|---|---|---|---|
| POST | `/api/prescriptions/` | Doctor/Admin | Create prescription |
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
| GET | `/api/dashboard/` | Admin | Get system analytics (Redis cached) |

---

## 🖥 Frontend

Responsive multi-page frontend served via Django's static files.

| Page | URL | Description |
|---|---|---|
| Login | `/static/login.html` | Login for all roles, auto-redirects by role |
| Register | `/static/register.html` | Register as Doctor or Patient |
| Admin Dashboard | `/static/admin_dashboard.html` | Stats, doctors, patients, billing |
| Doctor Dashboard | `/static/doctor_dashboard.html` | Appointments, prescriptions, profile |
| Patient Dashboard | `/static/patient_dashboard.html` | Book appointments, records, billing |

### Security
- Admin role is **not available** in the registration form
- Backend **validates and rejects** any API request attempting to register as admin
- Only a superuser can create admin accounts via the Django admin panel

---

## 🚀 Getting Started

### Prerequisites
- [Docker](https://www.docker.com/get-started) and Docker Compose
- [Git](https://git-scm.com/)

### Clone and Run
```bash
git clone https://github.com/YOUR_USERNAME/hospital-management-system.git
cd hospital-management-system

# Copy env file
cp .env.example .env

# Build and start
docker-compose up --build
```

Access at: **http://localhost:8000/static/login.html**

---

## ⚙️ Environment Variables

```env
SECRET_KEY=your-super-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=hospital_db
DB_USER=postgres
DB_PASSWORD=hospital_pass
DB_HOST=db
DB_PORT=5432
REDIS_URL=redis://redis:6379/1
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@hospital.com
DJANGO_SUPERUSER_PASSWORD=YourStrongPassword@123
```

---

## ☁️ Deployment

Deployed on **Render** using `render.yaml` blueprint.

```
Frontend  → https://hospital-management-system-y46v.onrender.com/static/login.html
API       → https://hospital-management-system-y46v.onrender.com/api/
Admin     → https://hospital-management-system-y46v.onrender.com/admin/
```

---

## 🔒 Security

- JWT auth with token blacklisting on logout
- **Admin registration blocked** at API and frontend level
- Role-based permissions on every endpoint
- `DEBUG=False` in production
- All secrets via environment variables
- HTTPS enforced via Render
- Password hashing via PBKDF2 + SHA256

---

## ⚡ Performance Optimizations

- Redis caching on dashboard (5-minute TTL)
- `select_related()` on all ViewSets (prevents N+1 queries)
- Django `Sum` aggregation for revenue calculation
- Pagination on all list endpoints (10 per page)
- Gunicorn with 3 workers
- Whitenoise compressed static files

---

## 🔮 Future Scope

- Celery for async email notifications
- React/Next.js frontend
- Load balancing with multiple instances
- Database read replicas
- Mobile app (React Native)

---

## 👨‍💻 Author

Built with ❤️ using Django REST Framework, Docker, PostgreSQL, Redis, and Vanilla JS.
