from uuid import UUID
from fastapi import Form
from pydantic import BaseModel


class SpecialityBase(BaseModel):
    name: str
    description: str
    area: str
    subjects: list

    class Config:
        from_attributes = True


class SpecialityUpdate(SpecialityBase):
    pass


class Speciality(SpecialityBase):
    id: UUID


class SpecialityCreate(Speciality):
    pass


class SpecialityTemplate(Speciality):
    pass


class SpecialityForm(SpecialityBase):

    @classmethod
    def as_form(
        cls,
        name: str = Form(),
        description: str = Form(),
        area: str = Form(),
        subjects: str = Form(),
    ):
        subjects = subjects.split(",")
        return cls(
            name=name,
            description=description,
            area=area,
            subjects=subjects,
        )
