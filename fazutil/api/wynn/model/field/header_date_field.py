from datetime import datetime

from dateutil import parser

from fazutil.api.wynn.model.field._date_field import DateField


class HeaderDateField(DateField):
    def __init__(self, datestr: str) -> None:
        super().__init__(datestr, "%a, %d %b %Y %H:%M:%S %Z")

    def to_datetime(self) -> datetime:
        return parser.parse(self.datestr)
