from sqlalchemy import select
from app.crud.crud_base import CRUDBase
from app import schemas
from app import models
from sqlalchemy.orm import Session


class CRUDEmployee(
    CRUDBase[models.Employee, schemas.EmployeeCreate, schemas.EmployeeUpdate]
):
    def get_by_email(self, db: Session, email: str) -> models.Employee | None:
        stmt = select(self.model).where(self.model.email == email)
        result = db.scalars(stmt).first()
        return result


employee = CRUDEmployee(models.Employee)
