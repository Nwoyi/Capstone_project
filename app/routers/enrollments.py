from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.enrollment import EnrollmentCreate, EnrollmentOut
from app.security import require_admin, require_student
from app.services import enrollment as enrollment_service

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])


@router.post(
    "",
    response_model=EnrollmentOut,
    status_code=status.HTTP_201_CREATED,
)
def enroll(
    payload: EnrollmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_student),
):
    return enrollment_service.enroll(
        db, user_id=current_user.id, course_id=payload.course_id
    )


@router.get("/me", response_model=list[EnrollmentOut])
def list_my_enrollments(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_student),
):
    return enrollment_service.list_my_enrollments(db, user_id=current_user.id)


@router.delete("/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
def deregister(
    enrollment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_student),
):
    enrollment_service.deregister(
        db, user_id=current_user.id, enrollment_id=enrollment_id
    )


@router.get(
    "",
    response_model=list[EnrollmentOut],
    dependencies=[Depends(require_admin)],
)
def admin_list_all(db: Session = Depends(get_db)):
    return enrollment_service.admin_list_all(db)


@router.get(
    "/by-course/{course_id}",
    response_model=list[EnrollmentOut],
    dependencies=[Depends(require_admin)],
)
def admin_list_for_course(course_id: int, db: Session = Depends(get_db)):
    return enrollment_service.admin_list_for_course(db, course_id)


@router.delete(
    "/admin/{enrollment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin)],
)
def admin_remove_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    enrollment_service.admin_remove_enrollment(db, enrollment_id)
