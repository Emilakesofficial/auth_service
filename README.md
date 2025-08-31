# 🛡️ Auth Service

A Django-based authentication microservice with **PostgreSQL**, **JWT authentication**, **Redis-powered password reset**, and **Docker support**. Built for scalable deployments on **Render**.  

---

## 🚀 Features

### 🔐 User Management
- Custom User model (Full Name, Email as username, Password).  
- Secure password storage with Django’s built-in hashing.  

### 🔑 Authentication
- Login with **JWT authentication**.  
- Registration with PostgreSQL persistence.  

### 🔄 Forgot Password with Redis
- Generate a secure reset token.  
- Store token in **Redis** with expiry (10 minutes).  
- Reset password using the token.  

### ⏳ Rate Limiting
- Protection against brute force on login & password reset endpoints.  

### 🐳 Dockerized Development
- Full **Docker + Docker Compose** support for local dev.  

### ☁️ Deployment Ready  

### 📖 API Documentation
- Integrated **Swagger UI** for exploring endpoints.  

---

## 🛠️ Tech Stack

- **Backend**: Django + Django REST Framework  
- **Auth**: JWT (via `djangorestframework-simplejwt`)  
- **Database**: PostgreSQL  
- **Cache**: Redis  
- **Containerization**: Docker + Docker Compose  
- **Deployment**: Render  

---

## ⚙️ Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/Emilakesofficial/auth_service
cd bill-auth

** 2. Create virtual environment (if not using Docker)
- python -m venv venv
- source venv/bin/activate  # Linux / Mac
- venv\Scripts\activate     # Windows

** 3. Install dependencies
- pip install -r requirements.txt

** 4. Configure Environment Variables

*** Create a .env file in the project root:
- SECRET_KEY=your_django_secret
- DEBUG=
- DATABASE_URL=
- REDIS_URL=

** 5. Run Migrations
- python manage.py migrate

** 6. Start Server
- python manage.py runserver

*** 🐳 Run with Docker 
- Build and start containers
- docker-compose up --build

Run migrations inside container
docker-compose exec web python manage.py migrate

Now visit 👉 http://localhost:8000

** API Endpoints
Auth

POST /api/auth/register/ – Register a new user.

POST /api/auth/login/ – Login with email + password, returns JWT.

POST /api/auth/forgot-password/ – Request reset token (stored in Redis).

POST /api/auth/reset-password/ – Reset password with token.


## 📖 API Documentation

- Swagger UI: `/api/docs/`
- ReDoc: `/api/redoc/`
- OpenAPI Schema: `/api/docs.json`






