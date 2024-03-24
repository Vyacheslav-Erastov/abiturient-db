from datetime import datetime
from uuid import UUID, uuid4
from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app import schemas
from app import crud
from app.api import dependencies as deps
from app.core.security import get_current_employee, get_current_enrollee
from app.core.context_manager import handle_db_exception

router = APIRouter()

templates = Jinja2Templates(directory="templates")


# @router.get("/")
def read_applications(db):
    db_applications = crud.application.get_multi(db=db)
    applications = []
    for db_application in db_applications:
        application = schemas.ApplicationDetailed.from_orm(db_application).model_dump()
        applications.append(application)
    return applications


@router.post("/")
def create_application(
    request: Request,
    enrollee=Depends(get_current_enrollee),
    application_in: schemas.ApplicationForm = Depends(schemas.ApplicationForm.as_form),
    db: Session = Depends(deps.get_db),
):
    try:
        application_create = schemas.ApplicationCreate(
            **application_in.model_dump(),
            enrollee_id=enrollee.id,
            registration_date=datetime.now(),
            id=uuid4()
        )
        application = crud.application.create(db=db, obj_in=application_create)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)
    return RedirectResponse(
        request.url_for("enrollee_start"), status_code=status.HTTP_303_SEE_OTHER
    )


@router.post("/multi", response_model=list[schemas.Application])
def create_applications(
    applications_in: list[schemas.ApplicationCreate],
    db: Session = Depends(deps.get_db),
):
    for application_in in applications_in:
        try:
            application_in.id = uuid4()
            application = crud.application.create(db=db, obj_in=application_in)
            db.commit()
        except Exception as e:
            db.rollback()
            print(e)
    return applications_in


@router.get("/")
def update_application(
    request: Request,
    application_id: UUID,
    new_status: str,
    employee=Depends(get_current_employee),
    db: Session = Depends(deps.get_db),
):
    if employee is None:
        return RedirectResponse(
            request.url_for("employee_start"), status_code=status.HTTP_303_SEE_OTHER
        )
    with handle_db_exception(db):
        application = crud.application.update_status(
            db=db, employee_id=employee.id, status=new_status, _id=application_id
        )
    return RedirectResponse(
        request.url_for("employee_applications_get"),
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.delete("/")
def delete_application(application_id: UUID, db: Session = Depends(deps.get_db)):
    crud.application.remove(db=db, _id=application_id)
    return application_id
