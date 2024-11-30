from typing import Annotated

from fastapi import Depends, Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, description='Номер стр.', ge=1)]
    per_page: Annotated[int | None, Query(3, description='Кол-во отелей на стр.', gt=1, lt=30)]


PaginationsDep = Annotated[PaginationParams, Depends()]