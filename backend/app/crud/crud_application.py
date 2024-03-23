from app.crud.crud_base import CRUDBase
from app import schemas
from app import models


class CRUDApplication(
    CRUDBase[models.Application, schemas.ApplicationCreate, schemas.ApplicationUpdate]
):
    pass


application = CRUDApplication(models.Application)
