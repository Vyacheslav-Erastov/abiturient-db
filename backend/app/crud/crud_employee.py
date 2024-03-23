from app.crud.crud_base import CRUDBase
from app import schemas
from app import models


class CRUDEmployee(
    CRUDBase[models.Employee, schemas.EmployeeCreate, schemas.EmployeeUpdate]
):
    pass


employee = CRUDEmployee(models.Employee)
