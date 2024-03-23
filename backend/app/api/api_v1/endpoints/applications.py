from uuid import UUID, uuid4
from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app import schemas
from app import crud
from app.api import dependencies as deps

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/")
def read_applications(
    request: Request,
    db: Session = Depends(deps.get_db),
):
    db_applications = crud.application.get_multi(db=db)
    applications = []
    for db_application in db_applications:
        application = schemas.ApplicationTemplate.from_orm(db_application).model_dump()
        applications.append(application)
    return templates.TemplateResponse(
        request=request,
        name="applications.html",
        context={"applications": applications},
    )


@router.post("/")
def create_application(
    request: Request,
    application_in: schemas.ApplicationCreate = Depends(
        schemas.ApplicationForm.as_form
    ),
    db: Session = Depends(deps.get_db),
):
    try:
        application = crud.application.create(db=db, obj_in=application_in)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)
    return RedirectResponse(
        request.url_for("read_applications"), status_code=status.HTTP_303_SEE_OTHER
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


@router.put("/{application_id}", response_model=schemas.Application)
def update_application(
    application_id: UUID,
    application_in: schemas.ApplicationUpdate,
    db: Session = Depends(deps.get_db),
):
    try:
        application = crud.application.update(
            db=db, obj_in=application_in, _id=application_id
        )
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)
    return application


@router.delete("/")
def delete_application(application_id: UUID, db: Session = Depends(deps.get_db)):
    crud.application.remove(db=db, _id=application_id)
    return application_id
