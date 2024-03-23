from typing import TYPE_CHECKING
from app.db.base_class import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.models.application import Application


class Employee(Base):
    __tablename__ = "employees"
    first_name: Mapped[str]
    second_name: Mapped[str]
    phone_number: Mapped[str]
    email: Mapped[str | None] = mapped_column(default=None)
    password: Mapped[str]
    applications: Mapped[list["Application"]] = relationship(back_populates="employee")
