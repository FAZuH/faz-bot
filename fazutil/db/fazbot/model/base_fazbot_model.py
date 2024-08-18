from sqlalchemy import MetaData

from ...base_model import BaseModel


class BaseFazbotModel(BaseModel):
    __abstract__ = True
    metadata = MetaData()
