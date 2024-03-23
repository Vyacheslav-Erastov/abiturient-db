from datetime import timedelta
from uuid import UUID, uuid4
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app import schemas
from app import crud
from app.api import dependencies as deps
from app.core.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_employee,
    create_access_token,
    get_current_employee,
    get_password_hash,
)

router = APIRouter()

templates = Jinja2Templates(directory="templates/employee")


# @router.get("/")
# def read_employees(
#     request: Request,
#     db: Session = Depends(deps.get_db),
# ):
#     db_employees = crud.employee.get_multi(db=db)
#     employees = []
#     for db_employee in db_employees:
#         employee = schemas.EmployeeTemplate.from_orm(db_employee).model_dump()
#         employees.append(employee)
#     return templates.TemplateResponse(
#         request=request, name="employees.html", context={"employees": employees}
#     )


@router.get("/")
def employee_start(
    request: Request,
    employee=Depends(get_current_employee),
):
    if employee is None:
        return templates.TemplateResponse(request=request, name="login.html")
    return templates.TemplateResponse(
        request=request, name="employee.html", context={"employee": employee}
    )


@router.get("/register")
def employee_register_get(request: Request):
    return templates.TemplateResponse(request=request, name="register.html")


@router.post("/register")
def employee_register(
    request: Request,
    employee_in: schemas.EmployeeBase = Depends(schemas.EmployeeForm.as_form),
    db: Session = Depends(deps.get_db),
):
    employee_in.password = get_password_hash(employee_in.password)
    employee_create = schemas.EmployeeCreate(**employee_in.model_dump(), id=uuid4())
    crud.employee.create(db=db, obj_in=employee_create)
    db.commit()
    return templates.TemplateResponse(request=request, name="login.html")


@router.get("/login")
def employee_login_get(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")


@router.get("/logout")
def employee_logout_get(request: Request):
    response = RedirectResponse(
        request.url_for("employee_start"), status_code=status.HTTP_303_SEE_OTHER
    )
    response.delete_cookie("token")
    return response


@router.post("/login")
def employee_login(
    request: Request,
    # response: Response,
    employee_in: schemas.EmployeeLogin = Depends(schemas.EmployeeLogin.as_form),
    db: Session = Depends(deps.get_db),
):

    employee = authenticate_employee(db, employee_in.email, employee_in.password)
    if not employee:
        response = RedirectResponse(
            request.url_for("employee_start"), status_code=status.HTTP_303_SEE_OTHER
        )
        return response
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": employee.email}, expires_delta=access_token_expires
    )
    response = RedirectResponse(
        request.url_for("employee_start"), status_code=status.HTTP_303_SEE_OTHER
    )
    response.set_cookie(key="token", value=access_token)
    return response


@router.post("/")
def create_employee(
    request: Request,
    employee_in: schemas.EmployeeCreate = Depends(schemas.EmployeeForm.as_form),
    db: Session = Depends(deps.get_db),
):
    try:
        employee = crud.employee.create(db=db, obj_in=employee_in)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)
    return RedirectResponse(
        request.url_for("read_employees"), status_code=status.HTTP_303_SEE_OTHER
    )


@router.post("/multi", response_model=list[schemas.Employee])
def create_employees(
    employees_in: list[schemas.EmployeeCreate],
    db: Session = Depends(deps.get_db),
):
    for employee_in in employees_in:
        try:
            employee_in.id = uuid4()
            employee = crud.employee.create(db=db, obj_in=employee_in)
            db.commit()
        except Exception as e:
            db.rollback()
            print(e)
    return employees_in


@router.put("/{employee_id}", response_model=schemas.Employee)
def update_employee(
    employee_id: UUID,
    employee_in: schemas.EmployeeUpdate,
    db: Session = Depends(deps.get_db),
):
    try:
        employee = crud.employee.update(db=db, obj_in=employee_in, _id=employee_id)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)
    return employee


@router.delete("/")
def delete_employee(employee_id: UUID, db: Session = Depends(deps.get_db)):
    crud.employee.remove(db=db, _id=employee_id)
    return employee_id
