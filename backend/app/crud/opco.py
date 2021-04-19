from app import models, schemas
from .base import CRUDBase


class CRUDOpco(CRUDBase[models.Opco, schemas.OpcoCreate, schemas.OpcoCreate]):
    pass


opco = CRUDOpco(models.Opco)
