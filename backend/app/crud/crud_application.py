from uuid import UUID

from sqlalchemy import update
from app.crud.crud_base import CRUDBase
from app import schemas
from app import models
from sqlalchemy.orm import Session


class CRUDApplication(
    CRUDBase[models.Application, schemas.ApplicationCreate, schemas.ApplicationUpdate]
):
    def update_status(
        self,
        db: Session,
        employee_id: UUID,
        status: models.ApplicationStatus,
        _id: UUID,
    ) -> models.Application:
        stmt = (
            update(self.model)
            .where(self.model.id == _id)
            .values(employee_id=employee_id, status=status)
            .returning(self.model)
        )
        result = db.scalars(stmt).first()
        return result


application = CRUDApplication(models.Application)
