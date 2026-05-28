from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.course import CourseCreate, CourseOut, CourseUpdate
from app.security import require_admin
from app.services import course as course_service

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.get("", response_model=list[CourseOut])
def list_courses(db: Session = Depends(get_db)):
    return course_service.list_courses(db, include_inactive=False)


@router.get("/{course_id}", response_model=CourseOut)
def get_course(course_id: int, db: Session = Depends(get_db)):
    return course_service.get_course(db, course_id)


@router.post(
    "",
    response_model=CourseOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)],
)
def create_course(payload: CourseCreate, db: Session = Depends(get_db)):
    return course_service.create_course(db, payload)


@router.put(
    "/{course_id}",
    response_model=CourseOut,
    dependencies=[Depends(require_admin)],
)
def update_course(
    course_id: int,
    payload: CourseUpdate,
    db: Session = Depends(get_db),
):
    return course_service.update_course(db, course_id, payload)


@router.patch(
    "/{course_id}/activate",
    response_model=CourseOut,
    dependencies=[Depends(require_admin)],
)
def activate_course(course_id: int, db: Session = Depends(get_db)):
    return course_service.set_active(db, course_id, is_active=True)


@router.patch(
    "/{course_id}/deactivate",
    response_model=CourseOut,
    dependencies=[Depends(require_admin)],
)
def deactivate_course(course_id: int, db: Session = Depends(get_db)):
    return course_service.set_active(db, course_id, is_active=False)


@router.delete(
    "/{course_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin)],
)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course_service.delete_course(db, course_id)
