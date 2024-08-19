from __future__ import annotations
from typing import TYPE_CHECKING

from .wynn import WynnApi

if TYPE_CHECKING:
    from .base_ratelimit_handler import BaseRatelimitHandler
    from .base_response import BaseResponse
