from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, Any, Self

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import ColumnProperty, DeclarativeBase, class_mapper

if TYPE_CHECKING:
    from sqlalchemy.sql.schema import Table


class BaseModel(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
    __column_attribute_names__ = None
    __primarykey_attribute_names__ = None

    _naming_convention = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    @classmethod
    def get_table(cls) -> Table:
        return cls.__table__  # type: ignore

    def clone(self) -> Self:
        return self.__class__(**self.to_dict())

    def to_dict(self, *, actual_column_names=True) -> dict[str, Any]:
        return (
            {k: getattr(self, k) for k in self.get_column_attribute_names()}
            if actual_column_names
            else {
                getattr(self.__class__, k).name: getattr(self, k)
                for k in self.get_column_attribute_names()
            }
        )

    @classmethod
    def get_column_attribute_names(
        cls, *, includes_primary_key: bool = True
    ) -> list[str]:
        if cls.__column_attribute_names__ is None:
            cls.__column_attribute_names__ = [
                p.key
                for p in class_mapper(cls).iterate_properties
                if isinstance(p, ColumnProperty)
                and (includes_primary_key or not p.columns[0].primary_key)
            ]
        return cls.__column_attribute_names__

    @classmethod
    def get_primarykey_attribute_names(cls) -> list[str]:
        if cls.__primarykey_attribute_names__ is None:
            cls.__primarykey_attribute_names__ = [
                p.key
                for p in class_mapper(cls).iterate_properties
                if isinstance(p, ColumnProperty) and p.columns[0].primary_key
            ]
        return cls.__primarykey_attribute_names__

    def __eq__(self, other: object) -> bool:
        for k, v in self.to_dict().items():
            v_other = getattr(other, k)
            if v != v_other:
                return False
        return True

    def __hash__(self) -> int:
        return hash(self.__repr__())

    def __repr__(self) -> str:
        items = self.to_dict()
        sorted_items = sorted(items.items(), key=lambda x: x[0])
        params = ", ".join(f"{k}={self._handle_repr_types(v)}" for k, v in sorted_items)
        return f"{self.__class__.__name__}({params})"

    @staticmethod
    def _handle_repr_types(obj: object):
        if isinstance(obj, Decimal):
            return float(obj)
        return obj
