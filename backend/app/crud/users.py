from app import models
from app import schemas
from typing import Any, Dict, Optional, Union
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from .base import CRUDBase


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
        create_data["hash_password"] = self.get_password_hash(
            create_data["password"])
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
