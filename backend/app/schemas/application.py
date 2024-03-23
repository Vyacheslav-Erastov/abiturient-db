from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID
from fastapi import Form
from pydantic import BaseModel
from app.models.application import ApplicationStatus
if TYPE_CHECKING:
    from app.schemas.enrollee import Enrollee
    from app.schemas.speciality import Speciality
    from app.schemas.employee import Employee


class ApplicationBase(BaseModel):
    enrollee_id: str
    employee_id: str
    speciality_id: str
    registration_date: datetime | None
    status: ApplicationStatus | None = ApplicationStatus.CREATED
    total_points: int

    class Config:
        from_attributes = True


class ApplicationUpdate(ApplicationBase):
    pass


class Application(ApplicationBase):
    id: UUID


class ApplicationCreate(Application):
    pass


class ApplicationTemplate(Application):
    pass


class ApplicationForm(ApplicationBase):

    @classmethod
    def as_form(
        cls,
        enrollee_id: str = Form(),
        employee_id: str = Form(),
        speciality_id: str = Form(),
        total_points: int = Form(),
    ):
        return cls(
            enrollee_id=enrollee_id,
            employee_id=employee_id,
            speciality_id=speciality_id,
            total_points=total_points,
        )


class ApplicationDetailed(Application):
    enrollee: "Enrollee"
    employee: "Employee"
    speciality: "Speciality"
