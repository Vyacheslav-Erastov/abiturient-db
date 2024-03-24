from uuid import UUID, uuid4
from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app import schemas
from app import crud
from app.api import dependencies as deps
from app.core.security import get_current_employee

router = APIRouter()


def read_specialities(db):
    db_specialities = crud.speciality.get_multi(db=db)
    specialities = []
    for db_speciality in db_specialities:
        speciality = schemas.Speciality.from_orm(db_speciality).model_dump()
        specialities.append(speciality)
    return specialities


@router.post("/")
def create_speciality(
    request: Request,
    speciality_in: schemas.SpecialityBase = Depends(schemas.SpecialityForm.as_form),
    employee=Depends(get_current_employee),
    db: Session = Depends(deps.get_db),
):
    try:
        if employee is None:
            return RedirectResponse(
                request.url_for("employee_start"), status_code=status.HTTP_303_SEE_OTHER
            )
        speciality_create = schemas.SpecialityCreate(
            **speciality_in.model_dump(), id=uuid4()
        )
        speciality = crud.speciality.create(db=db, obj_in=speciality_create)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)
    return RedirectResponse(
        request.url_for("employee_start"), status_code=status.HTTP_303_SEE_OTHER
    )


@router.post("/multi", response_model=list[schemas.Speciality])
def create_specialities(
    specialities_in: list[schemas.SpecialityCreate],
    db: Session = Depends(deps.get_db),
):
    for speciality_in in specialities_in:
        try:
            speciality_in.id = uuid4()
            speciality = crud.speciality.create(db=db, obj_in=speciality_in)
            db.commit()
        except Exception as e:
            db.rollback()
            print(e)
    return specialities_in


@router.put("/{speciality_id}", response_model=schemas.Speciality)
def update_speciality(
    speciality_id: UUID,
    speciality_in: schemas.SpecialityUpdate,
    db: Session = Depends(deps.get_db),
):
    try:
        speciality = crud.speciality.update(
            db=db, obj_in=speciality_in, _id=speciality_id
        )
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)
    return speciality


@router.delete("/")
def delete_speciality(speciality_id: UUID, db: Session = Depends(deps.get_db)):
    crud.speciality.remove(db=db, _id=speciality_id)
    return speciality_id
