# 🏥 Hospital Management System

A scalable, production-ready backend REST API built with **Django** and **Django REST Framework**, featuring role-based authentication, appointment booking, prescriptions, billing, Redis caching, and full Docker + Render deployment.

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Technology Stack](#technology-stack)
- [Features](#features)
- [Project Structure](#project-structure)
- [Database Design](#database-design)
- [API Endpoints](#api-endpoints)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [Running with Docker](#running-with-docker)
- [API Testing](#api-testing)
- [Deployment](#deployment)
- [Performance Optimizations](#performance-optimizations)
- [Security](#security)
- [Future Scope](#future-scope)

---

## 📌 Project Overview

The Hospital Management System is a backend application that manages hospital operations including doctor and patient management, appointment scheduling, prescriptions, and billing. It implements JWT-based authentication with role-based access control for three user types: **Admin**, **Doctor**, and **Patient**.

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
| Containerization | Docker, Docker Compose |
| Deployment | Render |

---

## ✨ Features

- **JWT Authentication** — Secure login, token refresh, and token blacklisting on logout
- **Role-Based Access Control** — Three roles: Admin, Doctor, Patient with scoped permissions
- **Doctor Management** — Profile management, specialization, availability, consultation fee
- **Patient Management** — Profile management, medical history, blood group
- **Appointment Booking** — Book appointments with double-booking prevention
- **Prescription Module** — JSON-based medication records linked to appointments
- **Billing & Invoicing** — Invoice creation, payment tracking, mark-as-paid functionality
- **Dashboard Analytics** — Aggregated stats with Redis caching (5-minute TTL)
- **Auto Profile Creation** — Doctor/Patient profiles auto-created via Django signals on registration
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
 │    ├── specialization
 │    ├── license_number
 │    ├── experience_years
 │    ├── consultation_fee
 │    └── is_available
 │
 └── Patient (OneToOne → User)
      ├── date_of_birth
      ├── blood_group
      ├── address
      ├── emergency_contact
      └── medical_history

Appointment (ForeignKey → Doctor, Patient)
 ├── appointment_date + appointment_time
 ├── status: pending | confirmed | completed | cancelled
 └── reason, notes

Prescription (OneToOne → Appointment)
 ├── diagnosis
 ├── medications (JSONField)
 ├── instructions
 └── follow_up_date

Invoice (OneToOne → Appointment)
 ├── amount, tax, discount, total_amount
 ├── payment_status: pending | paid | cancelled
 └── payment_method: cash | card | online | insurance
```

---

## 🔗 API Endpoints

### Auth
| Method | Endpoint | Access | Description |
|---|---|---|---|
| POST | `/api/auth/register/` | Public | Register new user |
| POST | `/api/auth/login/` | Public | Login, get JWT tokens |
| POST | `/api/auth/refresh/` | Public | Refresh access token |
| GET | `/api/auth/register/profile/` | Any | Get current user profile |
| POST | `/api/auth/register/logout/` | Any | Logout, blacklist token |

### Doctors
| Method | Endpoint | Access | Description |
|---|---|---|---|
| GET | `/api/doctors/` | Any | List all doctors |
| GET | `/api/doctors/{id}/` | Any | Get doctor detail |
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
| GET | `/api/appointments/` | Any | List own appointments |
| GET | `/api/appointments/{id}/` | Any | Get appointment detail |
| PATCH | `/api/appointments/{id}/update_status/` | Doctor/Admin | Update status |

### Prescriptions
| Method | Endpoint | Access | Description |
|---|---|---|---|
| POST | `/api/prescriptions/` | Doctor/Admin | Create prescription |
| GET | `/api/prescriptions/` | Any | List own prescriptions |
| GET | `/api/prescriptions/{id}/` | Any | Get prescription detail |

### Billing
| Method | Endpoint | Access | Description |
|---|---|---|---|
| POST | `/api/billing/` | Admin | Create invoice |
| GET | `/api/billing/` | Any | List own invoices |
| PATCH | `/api/billing/{id}/mark_paid/` | Admin | Mark invoice as paid |

### Dashboard
| Method | Endpoint | Access | Description |
|---|---|---|---|
| GET | `/api/dashboard/` | Admin | Get system analytics |

---

## 🚀 Getting Started

### Prerequisites

- [Docker](https://www.docker.com/get-started) and Docker Compose
- [Git](https://git-scm.com/)

### Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/hospital-management-system.git
cd hospital-management-system
```

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

# JWT
ACCESS_TOKEN_LIFETIME_MINUTES=60
REFRESH_TOKEN_LIFETIME_DAYS=7
```

---

## 🐳 Running with Docker

```bash
# Build and start all containers (Django + PostgreSQL + Redis)
docker-compose up --build

# Run in detached mode
docker-compose up --build -d

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Stop all containers
docker-compose down

# Stop and remove volumes (fresh start)
docker-compose down -v
```

Once running, access:
- **API** → http://localhost:8000/api/
- **Admin Panel** → http://localhost:8000/admin/

---

## 🧪 API Testing

Import the collection into **Postman** and test all endpoints.

### Quick Test Flow

**1. Register a doctor**
```bash
POST /api/auth/register/
{
    "username": "drjohn",
    "email": "drjohn@hospital.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "Test@1234",
    "password2": "Test@1234",
    "role": "doctor",
    "phone": "9999999999"
}
```

**2. Login and get token**
```bash
POST /api/auth/login/
{
    "username": "drjohn",
    "password": "Test@1234"
}
```

**3. Use token in all subsequent requests**
```
Authorization: Bearer <access_token>
```

**4. Book an appointment (patient token)**
```bash
POST /api/appointments/
{
    "doctor": 1,
    "patient": 1,
    "appointment_date": "2026-03-01",
    "appointment_time": "10:00:00",
    "reason": "Regular checkup"
}
```

---

## ☁️ Deployment

This project is deployed on **Render** using the `render.yaml` blueprint.

### Live URL
```
https://hospital-management-system.onrender.com
```

### Deploy your own

1. Push code to GitHub
2. Go to [render.com](https://render.com) → New → Blueprint
3. Connect your GitHub repo
4. Render auto-detects `render.yaml` and creates:
   - Web service (Docker)
   - PostgreSQL database
   - Redis instance
5. Add environment variables in Render dashboard
6. Deploy

---

## ⚡ Performance Optimizations

- **Redis Caching** — Dashboard stats cached for 5 minutes, reducing DB load
- **select_related()** — Used across all ViewSets to prevent N+1 queries
- **Aggregation Queries** — Revenue calculation uses Django's `Sum` aggregation
- **Pagination** — All list endpoints paginated (10 items per page)
- **Gunicorn** — 3 worker processes for concurrent request handling

---

## 🔒 Security

- JWT authentication with token blacklisting on logout
- Role-based access control on every endpoint
- `DEBUG=False` in production
- Secret key and credentials via environment variables
- Secure database connection via Render managed PostgreSQL
- HTTPS enforced in production via Render

---

## 🔮 Future Scope

- **Celery** — Async tasks for email notifications on appointment booking
- **Load Balancing** — Multiple web service instances
- **Database Read Replicas** — Separate read/write DB connections
- **Redis Clustering** — High availability cache
- **CDN Integration** — Static content delivery
- **Frontend** — React/Next.js frontend connecting to this API

---

## 👨‍💻 Author

Built with ❤️ using Django REST Framework, Docker, PostgreSQL, and Redis.