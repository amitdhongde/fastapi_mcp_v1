from typing import List
from fastapi import Query

def common_parameters(
        q: List[str] | None = Query(default=None, alias="q"),
        filter: List[str] | None = Query(default=None, alias="filter"),
        skip: int = Query(default=0, alias="skip"),
        limit: int = Query(default=100, alias="limit"),
        sort_by: str | None = Query(default=None, alias="sort_by"),
        sort_order: str | None = Query(default=None, alias="sort_order")
    ) -> dict:

    print (f"q: {q}, filter: {filter}, skip: {skip}, limit: {limit}, sort_by: {sort_by}, sort_order: {sort_order}")

    return {
            "q": q, "filter": filter,
            "skip": skip, "limit": limit,
            "sort_by": sort_by, "sort_order": sort_order
        }
