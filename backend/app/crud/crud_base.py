from typing import Generic, Optional, Type, TypeVar
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import Session

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, _id: UUID) -> Optional[ModelType]:
        stmt = select(self.model).where(self.model.id == _id)
        result = db.scalars(stmt).first()
        return result

    def get_multi(self, db: Session) -> list[ModelType]:
        stmt = select(self.model)
        result = db.scalars(stmt).all()
        return result

    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        stmt = insert(self.model).values(**obj_in.dict()).returning(self.model)
        result = db.scalars(stmt).first()
        return result

    def update(self, db: Session, obj_in: UpdateSchemaType, _id: UUID) -> ModelType:
        stmt = (
            update(self.model)
            .where(self.model.id == _id)
            .values(**obj_in.dict(exclude_unset=True))
            .returning(self.model)
        )
        result = db.scalars(stmt).first()
        return result

    def remove(self, db: Session, _id: UUID) -> UUID:
        stmt = delete(self.model).where(self.model.id == _id)
        db.execute(stmt)
        return _id
