from sqlalchemy import MetaData

from fazutil.db.base_model import BaseModel


class BaseFazwynnModel(BaseModel):
    __abstract__ = True
    metadata = MetaData(naming_convention=BaseModel._naming_convention)
