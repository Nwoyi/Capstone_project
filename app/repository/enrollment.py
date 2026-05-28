from sqlalchemy.orm import Session

from app.models.enrollment import Enrollment


def get_by_id(db: Session, enrollment_id: int) -> Enrollment | None:
    return db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()


def get_by_user_and_course(
    db: Session, user_id: int, course_id: int
) -> Enrollment | None:
    return (
        db.query(Enrollment)
        .filter(Enrollment.user_id == user_id, Enrollment.course_id == course_id)
        .first()
    )


def count_for_course(db: Session, course_id: int) -> int:
    return db.query(Enrollment).filter(Enrollment.course_id == course_id).count()


def list_for_user(db: Session, user_id: int) -> list[Enrollment]:
    return db.query(Enrollment).filter(Enrollment.user_id == user_id).all()


def list_all(db: Session) -> list[Enrollment]:
    return db.query(Enrollment).all()


def list_for_course(db: Session, course_id: int) -> list[Enrollment]:
    return db.query(Enrollment).filter(Enrollment.course_id == course_id).all()


def create(db: Session, user_id: int, course_id: int) -> Enrollment:
    enrollment = Enrollment(user_id=user_id, course_id=course_id)
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment


def delete(db: Session, enrollment: Enrollment) -> None:
    db.delete(enrollment)
    db.commit()
