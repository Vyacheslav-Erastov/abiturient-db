from datetime import timedelta
from uuid import UUID, uuid4
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app import schemas
from app import crud
from app.api import dependencies as deps
from app.core.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_enrollee,
    create_access_token,
    get_current_enrollee,
    get_password_hash,
)
from app.api.api_v1.endpoints.applications import read_applications
from app.core.context_manager import handle_db_exception
from app.api.api_v1.endpoints.specialities import read_specialities

router = APIRouter()

templates = Jinja2Templates(directory="templates/enrollee")


@router.get("/multi")
def read_enrollees(
    request: Request,
    db: Session = Depends(deps.get_db),
):
    db_enrollees = crud.enrollee.get_multi(db=db)
    enrollees = []
    for db_enrollee in db_enrollees:
        enrollee = schemas.EnrolleeTemplate.from_orm(db_enrollee).model_dump()
        enrollees.append(enrollee)
    return templates.TemplateResponse(
        request=request, name="enrollees.html", context={"enrollees": enrollees}
    )


@router.get("/applications")
def enrollee_applications_get(
    request: Request,
    db: Session = Depends(deps.get_db),
    enrollee=Depends(get_current_enrollee),
):
    applications = read_applications(db=db)
    specialities = read_specialities(db=db)
    return templates.TemplateResponse(
        request=request,
        name="applications.html",
        context={
            "applications": applications,
            "enrollee": enrollee,
            "specialities": specialities,
        },
    )


@router.get("/")
def enrollee_start(
    request: Request,
    enrollee=Depends(get_current_enrollee),
    db: Session = Depends(deps.get_db),
):
    if enrollee is None:
        return templates.TemplateResponse(request=request, name="login.html")
    specialities = read_specialities(db=db)
    return templates.TemplateResponse(
        request=request,
        name="enrollee.html",
        context={"enrollee": enrollee, "specialities": specialities},
    )


@router.get("/register")
def enrollee_register_get(request: Request):
    return templates.TemplateResponse(request=request, name="register.html")


@router.post("/register")
def enrollee_register(
    request: Request,
    enrollee_in: schemas.EnrolleeBase = Depends(schemas.EnrolleeForm.as_form),
    db: Session = Depends(deps.get_db),
):
    with handle_db_exception(db):
        enrollee_in.password = get_password_hash(enrollee_in.password)
        enrollee_create = schemas.EnrolleeCreate(**enrollee_in.model_dump(), id=uuid4())
        crud.enrollee.create(db=db, obj_in=enrollee_create)
    return templates.TemplateResponse(request=request, name="login.html")


@router.get("/login")
def enrollee_login_get(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")


@router.get("/logout")
def enrollee_logout_get(request: Request):
    response = RedirectResponse(
        request.url_for("enrollee_start"), status_code=status.HTTP_303_SEE_OTHER
    )
    response.delete_cookie("token")
    return response


@router.post("/login")
def enrollee_login(
    request: Request,
    # response: Response,
    enrollee_in: schemas.EnrolleeLogin = Depends(schemas.EnrolleeLogin.as_form),
    db: Session = Depends(deps.get_db),
):
    enrollee = authenticate_enrollee(db, enrollee_in.email, enrollee_in.password)
    if not enrollee:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": enrollee.email}, expires_delta=access_token_expires
    )
    response = RedirectResponse(
        request.url_for("enrollee_start"), status_code=status.HTTP_303_SEE_OTHER
    )
    response.set_cookie(key="token", value=access_token)
    return response


@router.post("/")
def create_enrollee(
    request: Request,
    enrollee_in: schemas.EnrolleeBase = Depends(schemas.EnrolleeForm.as_form),
    db: Session = Depends(deps.get_db),
):
    try:
        enrollee_create = schemas.EmployeeCreate(**enrollee_in.model_dump(), id=uuid4())
        crud.enrollee.create(db=db, obj_in=enrollee_create)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)
    return RedirectResponse(
        request.url_for("read_enrollees"), status_code=status.HTTP_303_SEE_OTHER
    )


@router.post("/multi", response_model=list[schemas.Enrollee])
def create_enrollees(
    enrollees_in: list[schemas.EnrolleeCreate],
    db: Session = Depends(deps.get_db),
):
    for enrollee_in in enrollees_in:
        try:
            enrollee_in.id = uuid4()
            enrollee = crud.enrollee.create(db=db, obj_in=enrollee_in)
            db.commit()
        except Exception as e:
            db.rollback()
            print(e)
    return enrollees_in


@router.put("/", response_model=schemas.Enrollee)
def update_enrollee(
    request: Request,
    enrollee_in: schemas.EnrolleeUpdate,
    enrollee=Depends(get_current_enrollee),
    db: Session = Depends(deps.get_db),
):
    with handle_db_exception(db):
        enrollee = crud.enrollee.update(db=db, obj_in=enrollee_in, _id=enrollee.id)
    return RedirectResponse(
        request.url_for("enrollee_start"), status_code=status.HTTP_303_SEE_OTHER
    )


@router.delete("/")
def delete_enrollee(enrollee_id: UUID, db: Session = Depends(deps.get_db)):
    crud.enrollee.remove(db=db, _id=enrollee_id)
    return enrollee_id
