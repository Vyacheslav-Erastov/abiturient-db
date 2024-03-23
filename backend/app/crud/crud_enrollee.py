from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.crud.crud_base import CRUDBase
from app import schemas
from app import models


class CRUDEnrollee(
    CRUDBase[models.Enrollee, schemas.EnrolleeCreate, schemas.EnrolleeUpdate]
):
    def get_by_email(self, db: Session, email: str) -> models.Enrollee | None:
        stmt = select(self.model).where(self.model.email == email)
        result = db.scalars(stmt).first()
        return result


enrollee = CRUDEnrollee(models.Enrollee)
