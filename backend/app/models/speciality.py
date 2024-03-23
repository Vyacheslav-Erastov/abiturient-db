from typing import TYPE_CHECKING
from sqlalchemy import JSON
from app.db.base_class import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.models.application import Application


class Speciality(Base):
    __tablename__ = "specialties"
    name: Mapped[str]
    description: Mapped[str]
    area: Mapped[str]
    subjects: Mapped[list] = mapped_column(type_=JSON)
    applications: Mapped[list["Application"]] = relationship(
        back_populates="speciality"
    )
