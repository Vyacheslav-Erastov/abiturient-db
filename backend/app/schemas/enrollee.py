from typing import TYPE_CHECKING
from uuid import UUID
from fastapi import Form
from pydantic import BaseModel

# from app.schemas.application import ApplicationDetailed

if TYPE_CHECKING:
    from app.schemas.application import Application


class EnrolleeBase(BaseModel):
    first_name: str
    second_name: str
    phone_number: str
    password: str | None
    email: str | None = None

    class Config:
        from_attributes = True


class EnrolleeUpdate(EnrolleeBase):
    pass


class Enrollee(EnrolleeBase):
    id: UUID


class EnrolleeCreate(Enrollee):
    pass


class EnrolleeTemplate(Enrollee):
    pass


class EnrolleeForm(EnrolleeBase):

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


class EnrolleeLogin(BaseModel):
    email: str
    password: str

    @classmethod
    def as_form(
        cls,
        email: str | None = Form(),
        password: str = Form(),
    ):
        return cls(email=email, password=password)


class EnrolleeDetailed(Enrollee):
    applications: list = []
