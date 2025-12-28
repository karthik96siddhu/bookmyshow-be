# BookMyShow Backend API

A FastAPI-based backend service for a movie ticket booking platform. This system manages theatres, screens, shows, seats, bookings, orders, and user authentication.

## 📋 Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Features](#features)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Database Migrations](#database-migrations)

## 📌 Overview

BookMyShow Backend is a comprehensive REST API for managing movie theatre operations and ticket bookings. It provides features for:

- User authentication and authorization
- Theatre and screen management
- Movie and show scheduling
- Seat management and availability tracking
- Booking and order processing
- Payment management
- Real-time seat locking mechanisms

## 🛠 Tech Stack

- **Framework**: FastAPI 0.121.2
- **Database**: SQLAlchemy 2.0.44 (ORM)
- **Migrations**: Alembic
- **Server**: Uvicorn 0.38.0
- **Authentication**: JWT-based auth
- **Validation**: Pydantic 2.12.4
- **Python Version**: 3.x

## 📁 Project Structure

```
bookmyshow-be/
├── app/
│   ├── core/                 # Core utilities and configuration
│   │   ├── auth.py          # Authentication logic
│   │   ├── config.py        # Configuration settings
│   │   └── security.py      # Security utilities
│   ├── db/
│   │   └── database.py      # Database connection and session setup
│   ├── models/              # SQLAlchemy database models
│   │   ├── user.py          # User model
│   │   ├── booking.py       # Booking model
│   │   ├── movie.py         # Movie model
│   │   ├── order.py         # Order model
│   │   ├── payment.py       # Payment model
│   │   ├── screen.py        # Screen model
│   │   ├── seat.py          # Seat model
│   │   ├── seat_lock.py     # Seat locking model
│   │   ├── show.py          # Show model
│   │   ├── theatre.py       # Theatre model
│   │   └── __init__.py
│   ├── routes/              # API endpoints
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── admin_theatre.py # Theatre management (admin)
│   │   ├── admin_show.py    # Show management (admin)
│   │   ├── admin_seat.py    # Seat management (admin)
│   │   ├── movie.py         # Movie endpoints
│   │   ├── screen.py        # Screen endpoints
│   │   ├── user_movies.py   # User movie interactions
│   │   ├── seat_map.py      # Seat mapping endpoints
│   │   └── order.py         # Order management
│   ├── schemes/             # Pydantic request/response schemas
│   │   ├── user.py
│   │   ├── movie.py
│   │   ├── screen.py
│   │   ├── seat.py
│   │   ├── show.py
│   │   ├── seat_lock.py
│   │   └── theatre.py
│   ├── main.py              # FastAPI application entry point
│   └── create_tables.py     # Database table creation utility
├── alembic/                 # Database migration files
│   ├── versions/            # Migration scripts
│   ├── env.py              # Alembic environment configuration
│   └── script.py.mako      # Migration template
├── alembic.ini             # Alembic configuration
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## ✨ Features

### 1. **User Management**

- User registration and authentication
- Role-based access control (Admin/User)
- User profile management

### 2. **Theatre Management** (Admin)

- Create and manage theatres
- View theatre details and associated screens

### 3. **Show Scheduling** (Admin)

- Create and manage movie shows
- Schedule shows across different screens and time slots
- Manage show pricing and availability

### 4. **Seat Management**

- Dynamically view available seats for a show
- Admin controls for seat configuration
- Real-time seat status tracking

### 5. **Booking System**

- Reserve seats for users
- Seat locking mechanism to prevent double booking
- Multiple seat selection for group bookings

### 6. **Order Management**

- Create and track orders
- Link bookings to orders
- Order status tracking

### 7. **Payment Processing**

- Payment record creation
- Payment status management
- Integration with booking and order systems

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- PostgreSQL or compatible SQL database

### Setup Steps

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd bookmyshow-be
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the root directory:

   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/bookmyshow
   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **Create database tables**
   ```bash
   python -c "from app.create_tables import create_tables; create_tables()"
   ```

## ▶️ Running the Application

Start the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

### Interactive API Documentation

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## 📚 API Documentation

### Authentication Endpoints

```bash
# User Registration
POST /auth/register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "1234567890",
  "password": "secure_password"
}

# User Login
POST /auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "secure_password"
}
```

### Theatre Management (Admin)

```bash
# Get all theatres
GET /admin/theatres

# Create a new theatre
POST /admin/theatres
Content-Type: application/json

{
  "name": "PVR Cinema",
  "location": "Downtown Mall",
  "city": "Mumbai"
}
```

### Movies

```bash
# Get all movies
GET /movies

# Get movie details
GET /movies/{movie_id}
```

### Shows

```bash
# Get shows for a movie
GET /shows?movie_id={movie_id}

# Get show details with seat availability
GET /shows/{show_id}
```

### Seat Management

```bash
# Get seat map for a show
GET /seat-map/{show_id}

# Get available seats
GET /seats/{show_id}
```

### Bookings & Orders

```bash
# Create a booking
POST /bookings
Content-Type: application/json

{
  "show_id": 1,
  "seat_ids": [1, 2, 3],
  "user_id": 1
}

# Get order details
GET /orders/{order_id}

# Create payment
POST /payments
Content-Type: application/json

{
  "order_id": 1,
  "amount": 300,
  "payment_method": "credit_card"
}
```

## 🗄️ Database Migrations

This project uses Alembic for database schema management.

### Running Migrations

```bash
# Apply all pending migrations
alembic upgrade head

# Create a new migration
alembic revision --autogenerate -m "description of changes"

# Rollback last migration
alembic downgrade -1

# View migration history
alembic current
alembic history
```

### Key Migrations

- `54141a314a71_added_order_model.py` - Added Order model
- `2df2cf61cdea_map_order_id_to_booking_model.py` - Linked Orders to Bookings
- `30032bba739a_add_user_id_to_seat_locks.py` - Enhanced seat locking
- `ed5ef0d5f56d_make_seat_locks_order_id_non_nullable.py` - Seat lock constraints
- `497741cd2e9c_added_payment_table.py` - Payment processing support

## 🔐 Authentication & Authorization

The API uses JWT (JSON Web Tokens) for authentication:

1. Users register or login to get an access token
2. Include the token in the `Authorization: Bearer <token>` header for protected endpoints
3. Admin endpoints are protected by role-based access control

## 📝 Key Models

### User

- Email and phone-based authentication
- Role-based access (user/admin)
- Timestamps for user creation

### Show

- Links to Movie, Theatre, and Screen
- Manages showtimes and pricing

### Booking

- Links to Show, Seat, and Order
- Tracks individual seat reservations

### Order

- Groups multiple bookings
- Payment processing status

### Seat Lock

- Prevents double booking during checkout
- Time-based expiration
- Linked to orders

## 🤝 Contributing

Guidelines for contributing to this project:

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes and commit: `git commit -m "Add your message"`
3. Push to the branch: `git push origin feature/your-feature`
4. Submit a pull request

## 📞 Support

For issues, questions, or contributions, please reach out to the development team.
