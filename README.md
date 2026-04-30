# 🏥 Hospital Management System

A scalable, production-ready full-stack application built with **Django REST Framework** on the backend and a **fully responsive HTML/CSS/JS frontend**. It manages hospital operations including doctor and patient management, appointment scheduling, prescriptions, and billing — with JWT authentication, role-based access control, Redis caching, and deployment on AWS EC2 with Docker and GitHub Actions CI/CD.

> 🌐 **Live Demo:** [https://nova-hospital.duckdns.org/static/login.html](https://nova-hospital.duckdns.org/static/login.html)

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
- [CI/CD Pipeline](#cicd-pipeline)
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
| Reverse Proxy | Nginx |
| Cloud | AWS EC2, AWS ECR |
| CI/CD | GitHub Actions |

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

### DevOps
- Dockerized all services (web, db, redis, nginx)
- GitHub Actions CI/CD pipeline (test → build → deploy)
- Docker images stored in AWS ECR
- Auto-deploy to AWS EC2 on every push to main

---

## 📁 Project Structure

```
hospital-management-system/
├── Dockerfile
├── docker-compose.yml
├── docker-compose.prod.yml
├── requirements.txt
├── manage.py
├── .env.example
├── .gitignore
├── README.md
│
├── .github/
│   └── workflows/
│       └── deploy.yml           ← CI/CD pipeline
│
├── nginx/
│   ├── Dockerfile
│   └── nginx.conf               ← Reverse proxy config
│
├── frontend/                    ← Responsive web frontend
│   ├── login.html
│   ├── register.html
│   ├── admin_dashboard.html
│   ├── doctor_dashboard.html
│   └── patient_dashboard.html
│
└── hospital/
    ├── settings.py
    ├── urls.py
    ├── wsgi.py
    └── apps/
        ├── accounts/
        ├── doctors/
        ├── patients/
        ├── appointments/
        ├── prescriptions/
        ├── billing/
        └── dashboard/
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
 ├── appointment_date + appointment_time
 ├── status: pending | confirmed | completed | cancelled
 └── reason, notes

Prescription (OneToOne → Appointment)
 ├── diagnosis
 ├── medications: JSONField
 └── instructions, follow_up_date

Invoice (OneToOne → Appointment)
 ├── amount, tax, discount
 ├── total_amount
 ├── payment_status: pending | paid | cancelled
 └── payment_method: cash | card | online | insurance
```

---

## 🔗 API Endpoints

### Auth
| Method | Endpoint | Access | Description |
|---|---|---|---|
| POST | `/api/auth/register/` | Public | Register as doctor or patient |
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

### Patients
| Method | Endpoint | Access | Description |
|---|---|---|---|
| GET | `/api/patients/` | Admin / Doctor | List all patients |
| GET | `/api/patients/me/` | Patient | Get own profile |
| PUT | `/api/patients/me/` | Patient | Update own profile |

### Appointments
| Method | Endpoint | Access | Description |
|---|---|---|---|
| POST | `/api/appointments/` | Patient | Book appointment |
| GET | `/api/appointments/` | Any | List own appointments |
| PATCH | `/api/appointments/{id}/update_status/` | Doctor / Admin | Update status |

### Billing
| Method | Endpoint | Access | Description |
|---|---|---|---|
| POST | `/api/billing/` | Admin | Create invoice |
| GET | `/api/billing/` | Any | List own invoices |
| PATCH | `/api/billing/{id}/mark_paid/` | Admin | Mark as paid |

### Dashboard
| Method | Endpoint | Access | Description |
|---|---|---|---|
| GET | `/api/dashboard/` | Admin | System analytics (Redis cached) |

---

## 🖥 Frontend

| Page | URL | Description |
|---|---|---|
| Login | `/static/login.html` | Role-based login |
| Register | `/static/register.html` | Doctor or Patient registration |
| Admin Dashboard | `/static/admin_dashboard.html` | Full system overview |
| Doctor Dashboard | `/static/doctor_dashboard.html` | Appointments and prescriptions |
| Patient Dashboard | `/static/patient_dashboard.html` | Book appointments and billing |

---

## 🚀 Getting Started

### Prerequisites
- Docker and Docker Compose
- Git

### Local Development

```bash
git clone https://github.com/Nova-Gupta/hospital-management-system.git
cd hospital-management-system

cp .env.example .env
# Edit .env with your values

docker-compose up --build
```

Visit: **http://localhost/static/login.html**

---

## ⚙️ Environment Variables

```env
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-ec2-ip

DB_NAME=hospital_db
DB_USER=hospital_user
DB_PASSWORD=your-password
DB_HOST=db
DB_PORT=5432

REDIS_URL=redis://redis:6379/1

ECR_REGISTRY=your-ecr-registry
ECR_REPOSITORY=hospital-management-system
IMAGE_TAG=latest
```

---

## 🐳 Running with Docker

```bash
# Start all containers
docker-compose up --build -d

# Stop containers
docker-compose down

# View logs
docker-compose logs -f
```

---

## ☁️ Deployment

Deployed on **AWS EC2** with Docker, Nginx, and GitHub Actions CI/CD.

### Live URLs

```
Frontend  →  https://nova-hospital.duckdns.org/static/login.html
API       →  https://nova-hospital.duckdns.org/api/
Admin     →  https://nova-hospital.duckdns.org/admin/
```

### Infrastructure
- **AWS EC2** — t2.micro Ubuntu 26.04 instance
- **AWS ECR** — Docker image registry
- **Docker Compose** — Container orchestration
- **Nginx** — Reverse proxy serving static files and proxying to Gunicorn

---

## 🔄 CI/CD Pipeline

Every push to `main` triggers the GitHub Actions pipeline:

```
Push to main
    ↓
1. test          → Run Django tests with PostgreSQL + Redis
    ↓
2. build-and-push → Build Docker image → Push to AWS ECR
    ↓
3. deploy        → SSH into EC2 → Pull new image → Restart containers
                   → Run migrations → Collect static files
```

### Required GitHub Secrets

| Secret | Description |
|---|---|
| `AWS_ACCESS_KEY_ID` | AWS IAM access key |
| `AWS_SECRET_ACCESS_KEY` | AWS IAM secret key |
| `AWS_REGION` | e.g. ap-south-1 |
| `ECR_REGISTRY` | ECR registry URL |
| `ECR_REPOSITORY` | ECR repository name |
| `EC2_HOST` | EC2 Elastic IP |
| `EC2_USER` | EC2 username (ubuntu) |
| `EC2_SSH_KEY` | EC2 private key (.pem contents) |

---

## 🔒 Security

| Measure | Implementation |
|---|---|
| Authentication | JWT with token blacklisting |
| Admin registration | Blocked at frontend and API level |
| Role enforcement | Permission classes on every endpoint |
| Secrets | All credentials via environment variables |
| Password hashing | Django PBKDF2 + SHA256 |

---

## ⚡ Performance Optimizations

| Optimization | Detail |
|---|---|
| Redis caching | Dashboard stats cached for 5 minutes |
| select_related() | Applied on all ViewSets |
| Gunicorn workers | 3 workers for concurrent requests |
| Whitenoise | Compressed static file serving |
| Nginx | Reverse proxy with static file caching |

---

## 🔮 Future Scope

- Domain name + SSL/HTTPS with Let's Encrypt
- Celery for async email notifications
- React / Next.js frontend
- Mobile app with React Native

---

## 👨‍💻 Author

Built with ❤️ using Django REST Framework, PostgreSQL, Redis, Docker, Nginx, AWS EC2, and GitHub Actions.