from datetime import datetime
from enum import Enum
from uuid import UUID

from sqlalchemy import ForeignKey
from app.db.base_class import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.enrollee import Enrollee
from app.models.employee import Employee
from app.models.speciality import Speciality


class ApplicationStatus(str, Enum):
    CREATED = "CREATED"
    UNDER_CONSIDARATION = "UNDER_CONSIDARATION"
    CONFIRMED = "CONFIRMED"


class Application(Base):
    __tablename__ = "applications"
    enrollee_id: Mapped[UUID] = mapped_column(
        ForeignKey("enrollees.id", ondelete="CASCADE")
    )
    employee_id: Mapped[UUID | None] = mapped_column(ForeignKey("employees.id"))
    speciality_id: Mapped[UUID] = mapped_column(ForeignKey("specialties.id"))
    registration_date: Mapped[datetime] = mapped_column(default=datetime.now())
    status: Mapped[ApplicationStatus] = mapped_column(default="CREATED")
    total_points: Mapped[int]
    enrollee: Mapped["Enrollee"] = relationship(
        back_populates="applications", cascade="delete, all"
    )
    employee: Mapped["Employee"] = relationship(back_populates="applications")
    speciality: Mapped["Speciality"] = relationship(back_populates="applications")
