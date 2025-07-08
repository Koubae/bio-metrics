from fastapi import Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    limit: int
    offset: int


def get_pagination_params(
    limit: int = Query(10, ge=1, le=5000, description="Number of items to return"),
    offset: int = Query(0, ge=0, description="Number of items to skip"),
) -> PaginationParams:
    return PaginationParams(limit=limit, offset=offset)
