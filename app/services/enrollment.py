from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.enrollment import Enrollment
from app.repository import course as course_repo
from app.repository import enrollment as enrollment_repo


def enroll(db: Session, user_id: int, course_id: int) -> Enrollment:
    course = course_repo.get_by_id(db, course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )
    if not course.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This course is not active, cannot enroll",
        )
    if enrollment_repo.get_by_user_and_course(db, user_id, course_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are already enrolled in this course",
        )
    if enrollment_repo.count_for_course(db, course_id) >= course.capacity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This course is full",
        )
    return enrollment_repo.create(db, user_id=user_id, course_id=course_id)


def list_my_enrollments(db: Session, user_id: int) -> list[Enrollment]:
    return enrollment_repo.list_for_user(db, user_id)


def deregister(db: Session, user_id: int, enrollment_id: int) -> None:
    enrollment = enrollment_repo.get_by_id(db, enrollment_id)
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found",
        )
    if enrollment.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only deregister your own enrollment",
        )
    enrollment_repo.delete(db, enrollment)


def admin_list_all(db: Session) -> list[Enrollment]:
    return enrollment_repo.list_all(db)


def admin_list_for_course(db: Session, course_id: int) -> list[Enrollment]:
    course = course_repo.get_by_id(db, course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )
    return enrollment_repo.list_for_course(db, course_id)


def admin_remove_enrollment(db: Session, enrollment_id: int) -> None:
    enrollment = enrollment_repo.get_by_id(db, enrollment_id)
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found",
        )
    enrollment_repo.delete(db, enrollment)
