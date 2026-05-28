# Course Enrollment Platform API

## Project Title
Design, Secure, and Test a Course Enrollment Platform Using FastAPI

## Project Overview
You are required to design and implement a secure, database-backed RESTful API using FastAPI for managing a course enrollment platform.

Unlike previous projects, this system must:

- Use authentication and authorization
- Use a relational database
- Enforce role-based access control
- Handle non-trivial business rules
- Include comprehensive automated tests
- Deploy your app to the cloud

This project simulates a real-world backend system and will be assessed accordingly.

## Core Concepts Being Assessed
- Authentication & authorization
- Database modeling and relationships
- Role-based access control (RBAC)
- API design and correctness
- Validation and error handling
- Automated testing (unit + integration)
- Code organization and maintainability

## Entities
Your system must include at least the following entities:

### 1. User
- `id`
- `name`
- `email`
- `hashed_password`
- `role` (student or admin)
- `is_active`

### 2. Course
- `id`
- `title`
- `code`
- `capacity`
- `is_active`

### 3. Enrollment
- `id`
- `user_id`
- `course_id`
- `created_at`

## Authentication & Authorization

### Authentication
- Implement authentication using JWT
- Users must be able to:
  - Register
  - Log in
- Passwords must be securely hashed

### Authorization (Role-Based Access Control)

| Action | Student | Admin |
|---|---|---|
| View courses | ✅ | ✅ |
| Enroll in course | ✅ | ❌ |
| Deregister from course | ✅ | ❌ |
| Create course | ❌ | ✅ |
| Update course | ❌ | ✅ |
| Delete course | ❌ | ✅ |
| View all enrollments | ❌ | ✅ |

## Functional Requirements

### 1. User Management
- Register a user
- Log in a user
- Retrieve user profile (authenticated)

**Rules:**
- Email must be unique
- Role must be validated
- Inactive users cannot authenticate

### 2. Course Management
- Retrieve all active courses (public)
- Retrieve a course by ID (public)

**Admin-only:**
- Create a course
- Update course details
- Activate/deactivate a course

**Rules:**
- `code` must be unique
- `capacity` must be greater than zero

### 3. Enrollment Management
- Enroll a student in a course
- Deregister a student from a course

**Rules:**
- Only authenticated students can enroll
- A student cannot enroll in the same course twice
- Enrollment fails if the course is full
- Enrollment fails if the course is inactive

### 4. Administrative Oversight
Admins must be able to:

- View all enrollments
- View enrollments for a specific course
- Remove a student from a course

## Database Requirements
- Use a relational database (e.g. PostgreSQL)
- Properly define relationships between entities
- Use migrations
- Avoid raw SQL for business logic

## Validation & Error Handling
- Validate all incoming data using request models
- Return meaningful error messages
- Handle edge cases gracefully
- Ensure consistent API responses

## Testing Requirements (Strict)
You must write automated tests covering:

### API Tests
- Write tests for all endpoints

> ⚠️ **Important:** Failing tests or missing test coverage will result in penalties.

## Technical Expectations
- Clean project structure
- Clear separation of concerns
- Reusable dependencies
- Proper use of FastAPI dependency injection
- Secure handling of authentication data

## What Is NOT Required
- Frontend application
- Email notifications
- Payment systems
- Deployment configuration

## Submission Requirements
You must submit:

- Complete FastAPI project
- Database migration files
- Automated test suite
- `README.md` explaining:
  - Setup instructions
  - How to run migrations
  - How to run tests

## Assessment Criteria

| Area | Weight |
|---|---|
| Authentication & Security | 20% |
| Database Design | 20% |
| Business Logic Correctness | 25% |
| Code Quality & Structure | 15% |
| Testing | 15% |

## Optional Extensions (Bonus)
- Pagination & filtering
- Soft deletes
- Audit logs for enrollments
- Rate limiting on authentication endpoints

## Grading Guide

- **README** – Check if the user includes relevant information such as cloning and starting the application. **3 marks**
- **User management** – Includes register, login and user profile. **6 marks**
- **Course management read (public)** – Course management endpoints with public access. **4 marks**
- **Course management write (admin only access)** – **6 marks**
- **Enrollment management** – Correct enrolling to a course: **6 marks**. Deregistering from a course: **2 marks**. **Total: 8 marks**
- **Administrative oversight** – **9 marks**
- **Database setup and requirements** – **4 marks**
- **Data validation and error handling** – **4 marks**
- **API Testing** – For every endpoint without test case, deduct one mark. Minimum test case per endpoint is one. Maximum: **10 marks**
- **Code structure** – Services and repository API design should be followed. Folders for services, schemas, repository (DB access) and routers. **4 marls**

**Highest score a student can get is 58**
