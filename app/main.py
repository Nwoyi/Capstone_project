from fastapi import FastAPI

from app.routers import auth, courses, enrollments, users

app = FastAPI(
    title="Philip Course Enrollment Platform API",
    description="AltSchool Capstone Project Backend for a course enrollment system.",
    version="0.1.0",
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(courses.router)
app.include_router(enrollments.router)
