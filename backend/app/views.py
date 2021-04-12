from datetime import datetime, timedelta, date
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Body, UploadFile, File, Query
from fastapi.encoders import jsonable_encoder
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from pydantic.networks import EmailStr
from sqlalchemy.orm.session import Session
from app import schemas, models, crud, deps
from app.config import settings
from jose import jwt
from app.utils import generate_password_reset_token, send_reset_password_email, verify_password_reset_token

user_router = APIRouter(prefix='/users', tags=['users'])


@user_router.get('/', response_model=List[schemas.User])
def read_users(
    db: Session = Depends(deps.get_db),
    current_user: models.Users = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve users.
    """
    users = crud.user.get_multi(db)
    return users


@user_router.post("/", response_model=schemas.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
    current_user: models.Users = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new user.
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    return user


@user_router.put("/me", response_model=schemas.User)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    password: str = Body(None),
    full_name: str = Body(None),
    email: EmailStr = Body(None),
    current_user: models.Users = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if full_name is not None:
        user_in.full_name = full_name
    if email is not None:
        user_in.email = email
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@user_router.get("/me", response_model=schemas.User)
def read_user_me(
    db: Session = Depends(deps.get_db),
    current_user: models.Users = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@user_router.get("/{user_id}", response_model=schemas.User)
def read_user_by_id(
    user_id: int,
    current_user: models.Users = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = crud.user.get(db, id=user_id)
    if user == current_user:
        return user
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return user


@user_router.put("/{user_id}", response_model=schemas.User)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    user_in: schemas.UserUpdate,
    current_user: models.Users = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a user.
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return user


login_router = APIRouter(prefix='/login', tags=['login'])


@login_router.post("/access-token", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = datetime.utcnow(
    ) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": jwt.encode({"exp": access_token_expires, "sub": str(user.id)}, settings.SECRET_KEY),
        "token_type": "bearer",
    }


@login_router.post("/password-recovery/{email}", response_model=schemas.Msg)
def recover_password(email: str, db: Session = Depends(deps.get_db)) -> Any:
    """
    Password Recovery
    """
    user = crud.user.get_by_email(db, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    password_reset_token = generate_password_reset_token(email=email)
    send_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )
    return {"msg": "Password recovery email sent"}


@login_router.post("/reset-password/", response_model=schemas.Msg)
def reset_password(
    token: str = Body(...),
    new_password: str = Body(...),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Reset password
    """
    email = verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = crud.user.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    hashed_password = crud.user.get_password_hash(new_password)
    user.hashed_password = hashed_password
    db.add(user)
    db.commit()
    return {"msg": "Password updated successfully"}


report_router = APIRouter(prefix='/report', tags=['report'])


@report_router.get('/', response_model=List[schemas.Report])
def read_report(
    db: Session = Depends(deps.get_db),
    dt: date = date.today(),
    current_user: models.Users = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve report.
    """
    return crud.report.get_multu_by_user(db, dt=dt, user=current_user)


@report_router.post('/uploadfile')
def upload(db: Session = Depends(deps.get_db),
           file: UploadFile = File(...),
           current_user: models.Users = Depends(
               deps.get_current_active_superuser),
           ) -> Any:
    crud.report.loadfromfile(db, file.file._file)
    return {'detail': f'File {file.filename} imported.'}


@report_router.delete('/delete')
def delete(
    db: Session = Depends(deps.get_db),
    dt: date = Query(None),
    current_user: models.Users = Depends(
        deps.get_current_active_superuser),
) -> Any:
    crud.report.delete(db, dt)
    return {'detail': 'Rows deleted.'}


@report_router.get('/opco', response_model=List[schemas.Opco])
def read_opco(
    db: Session = Depends(deps.get_db),
    current_user: models.Users = Depends(deps.get_current_active_superuser),
) -> Any:
    return crud.opco.get_multi(db)
