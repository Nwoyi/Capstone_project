from sqlalchemy.orm import Session

from app.models.course import Course


def get_by_id(db: Session, course_id: int) -> Course | None:
    return db.query(Course).filter(Course.id == course_id).first()


def get_by_code(db: Session, code: str) -> Course | None:
    return db.query(Course).filter(Course.code == code).first()


def list_all(db: Session, include_inactive: bool = False) -> list[Course]:
    query = db.query(Course)
    if not include_inactive:
        query = query.filter(Course.is_active == True)
    return query.all()


def create(db: Session, title: str, code: str, capacity: int) -> Course:
    course = Course(title=title, code=code, capacity=capacity)
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


def save(db: Session, course: Course) -> Course:
    db.commit()
    db.refresh(course)
    return course


def delete(db: Session, course: Course) -> None:
    db.delete(course)
    db.commit()
