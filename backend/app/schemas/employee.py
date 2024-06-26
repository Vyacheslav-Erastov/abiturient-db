from typing import TYPE_CHECKING
from uuid import UUID
from fastapi import Form
from pydantic import BaseModel

# if TYPE_CHECKING:
#     from app.schemas.application import Application

# from app.schemas.application import ApplicationDetailed


class EmployeeBase(BaseModel):
    first_name: str
    second_name: str
    phone_number: str
    email: str | None = None
    password: str

    class Config:
        from_attributes = True


class EmployeeUpdate(EmployeeBase):
    pass


class Employee(EmployeeBase):
    id: UUID


class EmployeeCreate(Employee):
    pass


class EmployeeTemplate(Employee):
    id: UUID


class EmployeeForm(EmployeeBase):

    @classmethod
    def as_form(
        cls,
        first_name: str = Form(),
        second_name: str = Form(),
        phone_number: str = Form(),
        email: str | None = Form(),
        password: str = Form(),
    ):
        return cls(
            first_name=first_name,
            second_name=second_name,
            phone_number=phone_number,
            email=email,
            password=password,
        )


class EmployeeLogin(BaseModel):
    email: str
    password: str

    @classmethod
    def as_form(
        cls,
        email: str | None = Form(),
        password: str = Form(),
    ):
        return cls(email=email, password=password)


class EmployeeDetailed(Employee):
    applications: list = []
