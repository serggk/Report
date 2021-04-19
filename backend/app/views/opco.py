from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.session import Session
from app import schemas, models, crud, deps

opco_router = APIRouter(prefix='/opco', tags=['opco'])


@opco_router.get('/', response_model=List[schemas.Opco])
def read_report(
    db: Session = Depends(deps.get_db),
    current_user: models.Users = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve OpCo.
    """
    return crud.opco.get_multi(db)


@opco_router.post('/', response_model=schemas.Opco)
def create_opco(
    db: Session = Depends(deps.get_db),
    *,
    opco_in: schemas.OpcoCreate,
    current_user: models.Users = Depends(deps.get_current_active_superuser),
) -> Any:
    return crud.opco.create(db, opco_in)


@opco_router.get('/{opco_id}', response_model=schemas.Opco)
def read_opco(
    db: Session = Depends(deps.get_db),
    *,
    opco_id: int,
    current_user: models.Users = Depends(deps.get_current_active_superuser),
) -> Any:
    return crud.opco.get(db, opco_id)


@opco_router.put('/{opco_id}', response_model=schemas.Opco)
def update_opco(
    db: Session = Depends(deps.get_db),
    *,
    opco_id: int,
    opco_in: schemas.OpcoCreate,
    current_user: models.Users = Depends(deps.get_current_active_superuser),
) -> Any:
    opco = crud.opco.get(db, id=opco_id)
    if not opco:
        raise HTTPException(
            status_code=404,
            detail="The OpCo does not exist in the system",
        )
    opco = crud.opco.update(db, db_obj=opco, obj_in=opco_in)
    return opco


@opco_router.delete('/{opco_id}', response_model=schemas.Opco)
def remove_opco(
    db: Session = Depends(deps.get_db),
    *,
    opco_id: int,
    current_user: models.Users = Depends(deps.get_current_active_superuser),
) -> Any:
    return crud.opco.remove(db, opco_id)
