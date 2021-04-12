from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app import models, crud, schemas

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    models.Base.metadata.create_all(engine)
    db = SessionLocal()
    user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = schemas.UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
            is_active=True
        )
        user = crud.user.create(db, obj_in=user_in)
    db.commit()
    db.close()
