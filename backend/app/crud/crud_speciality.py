from app.crud.crud_base import CRUDBase
from app import schemas
from app import models


class CRUDSpeciality(
    CRUDBase[models.Speciality, schemas.SpecialityCreate, schemas.SpecialityUpdate]
):
    pass


speciality = CRUDSpeciality(models.Speciality)
