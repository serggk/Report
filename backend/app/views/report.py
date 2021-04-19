from datetime import date
from typing import Any, List
from fastapi import APIRouter, Depends, UploadFile, File, Query
from sqlalchemy.orm.session import Session
from app import schemas, models, crud, deps

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
