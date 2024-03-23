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
    enrollee_id: UUID
    employee_id: UUID
    speciality_id: UUID
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
    speciality_id: UUID
    total_points: int

    @classmethod
    def as_form(
        cls,
        speciality_id: UUID = Form(),
        total_points: int = Form(),
    ):
        return cls(
            speciality_id=speciality_id,
            total_points=total_points,
        )


class ApplicationDetailed(Application):
    enrollee: "Enrollee"
    employee: "Employee"
    speciality: "Speciality"
