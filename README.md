# Course Enrollment Platform API

AltSchool Capstone Project — a secure, database-backed REST API for managing course enrollments. Built with FastAPI, SQLAlchemy, and PostgreSQL (SQLite for local dev).

## Features

- JWT-based authentication
- Role-based access control (student / admin)
- Course catalogue with admin-only write access
- Enrollment with capacity and duplicate-protection rules
- Administrative oversight of enrollments
- Alembic migrations
- Automated tests with pytest

## Tech Stack

- **FastAPI** — web framework
- **SQLAlchemy 2.x** — ORM
- **Alembic** — database migrations
- **SQLite** (local dev) / **PostgreSQL** (production on Neon)
- **PyJWT** — JWT tokens
- **bcrypt** — password hashing
- **pytest** — testing

## Setup

### 1. Clone

```bash
git clone <your-repo-url>
cd Capstone_project
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv venv

# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure environment variables

Copy the example file and fill it in:

```bash
cp .env.example .env
```

Generate a secure JWT secret:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Paste the output as the value of `JWT_SECRET` in `.env`.

For local development, leave `DATABASE_URL` unset (the app falls back to SQLite). For production, set it to a PostgreSQL connection string (e.g. from Neon).

### 4. Run database migrations

```bash
alembic upgrade head
```

This creates the tables (`users`, `courses`, `enrollments`) in your database.

### 5. Create the first admin

`/auth/register` only creates **students**. Admin accounts are seeded via a CLI script so the role cannot be granted from the public API.

Set the admin credentials in your `.env`:

```env
ADMIN_NAME=Your Name
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=a-strong-password
```

Then run:

```bash
python -m app.scripts.create_admin
```

The script is idempotent — running it a second time with the same email prints "already exists" and exits cleanly.

### 6. Run the app

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## API Documentation

Interactive Swagger UI: `http://127.0.0.1:8000/docs`

ReDoc: `http://127.0.0.1:8000/redoc`

## Endpoints

### Authentication
| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/auth/register` | Public | Register a new student (admins are seeded via the CLI script) |
| POST | `/auth/login` | Public | Log in and receive a JWT |

### Users
| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/users/me` | Any logged-in user | Get current user profile |

### Courses
| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/courses` | Public | List active courses |
| GET | `/courses/{id}` | Public | Get a course by ID |
| POST | `/courses` | Admin | Create a course |
| PUT | `/courses/{id}` | Admin | Update a course |
| PATCH | `/courses/{id}/activate` | Admin | Activate a course |
| PATCH | `/courses/{id}/deactivate` | Admin | Deactivate a course |
| DELETE | `/courses/{id}` | Admin | Delete a course (blocked if enrollments exist) |

### Enrollments
| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/enrollments` | Student | Enroll in a course |
| GET | `/enrollments/me` | Student | List my enrollments |
| DELETE | `/enrollments/{id}` | Student | Deregister from own enrollment |
| GET | `/enrollments` | Admin | List all enrollments |
| GET | `/enrollments/by-course/{course_id}` | Admin | List enrollments for a course |
| DELETE | `/enrollments/admin/{enrollment_id}` | Admin | Admin removes any enrollment |

## Running Tests

```bash
pytest
```

Expected output: **30 passed**.

## Test Coverage

- **Auth** — register, duplicate-email, login, wrong password, `/me` requires auth, `/me` returns user
- **Courses** — public listing, admin-only writes, duplicate-code rejection, capacity validation, partial updates, activate/deactivate visibility
- **Enrollments** — student enroll, admin-cannot-enroll, double-enrollment blocked, inactive-course blocked, capacity enforced, list mine, deregister own, admin list all, admin remove any

## Project Structure

```
Capstone_project/
├── alembic/             # Database migrations
│   └── versions/
├── app/
│   ├── main.py          # FastAPI app entry point
│   ├── database.py      # DB engine, session, get_db dependency
│   ├── security.py      # Password hashing, JWT, auth dependencies
│   ├── models/          # SQLAlchemy models (tables)
│   ├── schemas/         # Pydantic schemas (request/response)
│   ├── repository/      # Database query layer
│   ├── services/        # Business logic
│   └── routers/         # API endpoints
├── tests/               # Pytest test suite
├── alembic.ini
├── requirements.txt
└── README.md
```

## Deployment

The app is deployed at: `<your-render-url-here>`

## Author

Philip — AltSchool Africa, Backend Engineering Track
