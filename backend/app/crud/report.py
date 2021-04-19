import datetime
from app import models
from app import schemas
from typing import Any, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from io import IOBase
from app.config import settings
import pandas as pd

from .base import CRUDBase

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
            opco = db.query(models.Opco).filter(func.lower(models.Opco.title) == func.lower(report_from_file['opco'])).first()
            if not opco:
                opco = models.Opco(title=report_from_file['opco'])
                db.add(opco)
            report = models.Report(**report_from_file)
            db.add(report)
        db.commit()
        return

    def delete(self, db: Session, dt: datetime.date) -> Any:
        db.query(models.Report).filter(models.Report.date == dt).delete()
        db.commit()
        return


report = CRUDReport(models.Report)

