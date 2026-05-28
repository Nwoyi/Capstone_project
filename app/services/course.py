from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.course import Course
from app.repository import course as course_repo
from app.repository import enrollment as enrollment_repo
from app.schemas.course import CourseCreate, CourseUpdate


def _get_course_or_404(db: Session, course_id: int) -> Course:
    course = course_repo.get_by_id(db, course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )
    return course


def list_courses(db: Session, include_inactive: bool = False) -> list[Course]:
    return course_repo.list_all(db, include_inactive=include_inactive)


def get_course(db: Session, course_id: int) -> Course:
    return _get_course_or_404(db, course_id)


def create_course(db: Session, payload: CourseCreate) -> Course:
    if course_repo.get_by_code(db, payload.code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A course with this code already exists",
        )
    return course_repo.create(
        db,
        title=payload.title,
        code=payload.code,
        capacity=payload.capacity,
    )


def update_course(db: Session, course_id: int, payload: CourseUpdate) -> Course:
    course = _get_course_or_404(db, course_id)

    if payload.code is not None and payload.code != course.code:
        if course_repo.get_by_code(db, payload.code):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A course with this code already exists",
            )
        course.code = payload.code

    if payload.title is not None:
        course.title = payload.title

    if payload.capacity is not None:
        course.capacity = payload.capacity

    return course_repo.save(db, course)


def set_active(db: Session, course_id: int, is_active: bool) -> Course:
    course = _get_course_or_404(db, course_id)
    course.is_active = is_active
    return course_repo.save(db, course)


def delete_course(db: Session, course_id: int) -> None:
    course = _get_course_or_404(db, course_id)
    if enrollment_repo.count_for_course(db, course_id) > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete a course with active enrollments. "
            "Remove enrollments first, or deactivate the course instead.",
        )
    course_repo.delete(db, course)
