import datetime
from app import models
from app import schemas
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext
from io import IOBase, TextIOWrapper
from app.config import settings
import pandas as pd


ModelType = TypeVar("ModelType", bound=models.Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).get(id)

    def get_multi(
        self, db: Session
    ) -> List[ModelType]:
        return db.query(self.model).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        # obj_in_data = obj_in
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        # obj_data = db_obj
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj


class CRUDUsers(CRUDBase[models.Users, schemas.UserCreate, schemas.UserUpdate]):
    def __init__(self, *args, **kwargs):
        super(CRUDUsers, self).__init__(*args, **kwargs)
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password: str, hash_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hash_password)

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def get_by_email(self, db: Session, *, email: str) -> Optional[models.Users]:
        return db.query(models.Users).filter(models.Users.email == email).first()

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[models.Users]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not self.verify_password(password, user.hash_password):
            return None
        return user

    def create(self, db: Session, *, obj_in: schemas.UserCreate) -> models.Users:
        if isinstance(obj_in, dict):
            create_data = obj_in
        else:
            create_data = obj_in.dict()
        create_data["hash_password"] = self.get_password_hash(create_data["password"])
        if create_data.get('opco', None):
            create_data['opco_id'] = create_data['opco']['id']
        del create_data["password"]
        del create_data["opco"]
        return super().create(db, obj_in=create_data)

    def update(
        self, db: Session, *, db_obj: models.Users, obj_in: Union[schemas.UserUpdate, Dict[str, Any]]
    ) -> models.Users:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data.get("password", None):
            hash_password = self.get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hash_password"] = hash_password
        if update_data.get("opco", None):
            update_data["opco_id"] = update_data["opco"]["id"]
        else:
            update_data["opco_id"] = None
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def is_active(self, user: models.Users) -> bool:
        return user.is_active

    def is_superuser(self, user: models.Users) -> bool:
        return user.is_superuser


user = CRUDUsers(models.Users)


class CRUDReport(CRUDBase[models.Report, schemas.Report, schemas.Report]):
    def get_multu_by_user(self, db: Session, dt: datetime.date, user: models.Users) -> List[models.Report]:
        if user.is_superuser:
            return db.query(self.model).filter_by(date=dt).all()
        return db.query(self.model).filter_by(opco=user.opco, date=dt).all()

    def loadfromfile(self, db: Session, file: IOBase) -> Any:
        # reader = pd.read_csv(file, dtype=settings.REPORT_CSV_PANDAS_TYPES)
        reader = pd.read_csv(file)
        for _, row in reader.iterrows():
            report_from_file = schemas.ReportFile(
                **{k: row[v] for k, v in settings.REPORT_MAPPING.items()}).dict()
            opco = db.query(models.Opco).filter_by(
                title=report_from_file['opco']).first()
            if opco:
                report_from_file['opco'] = opco
            else:
                report_from_file['opco'] = models.Opco(
                    title=report_from_file['opco'])
            report = models.Report(**report_from_file)
            db.add(report)
        db.commit()
        return

    def delete(self, db: Session, dt: datetime.date) -> Any:
        db.query(models.Report).filter(models.Report.date == dt).delete()
        db.commit()
        return


report = CRUDReport(models.Report)


class CRUDOpco(CRUDBase[models.Opco, schemas.Opco, schemas.Opco]):
    pass


opco = CRUDOpco(models.Opco)
