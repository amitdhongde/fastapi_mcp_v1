# from fastapi import APIRouter, Depends
# from modules.base.exceptions.base import InvalidTokenException
# from modules.user.controllers.controller import UserController

# # Import middlewares
# from modules.base.fastapi.dependencies.authentication import AuthGuard

# router = APIRouter(prefix="/users", tags=["Users"])

# @router.get("/", dependencies=[Depends(AuthGuard)])
# async def index():
#     return await UserController().index()

# @router.get("/{hash}")
# async def show(hash: str):
#     return await UserController().show(hash)

# @router.post("/")
# async def create():
#     return await UserController().create()

# @router.put("/{hash}")
# async def update(hash: str):
#     return await UserController().update(hash)

# @router.delete("/{hash}", dependencies=[Depends(AuthGuard)])
# async def delete(hash: str):
#     return await UserController().delete(hash)

""" Import the required modules """
from typing import Annotated, Any
from fastapi import APIRouter, Depends, Request

# Import middlewares and dependencies
from modules.base.fastapi.dependencies import (
    common_parameters
)

# Import middlewares and dependencies
from modules.base.fastapi.dependencies.authentication import AuthGuard

# Include the project controllers
from ..controllers import UserController as Controller

# Include the project models
from ..models import (
    UserCreateRequest,
    UserUpdateRequest
)

# Include the project exceptions
from modules.base.exceptions import (
    InvalidTokenException
)

router = APIRouter(prefix="/user", tags=["Users"])

@router.get("/",
        dependencies=[
            Depends(AuthGuard),
            Depends(common_parameters)
        ],
        name="get_users",
        operation_id="get_user_list"
    )
async def index(
        commons: Annotated[dict, Depends(common_parameters)],
        request: Request,
        auth: AuthGuard = Depends(AuthGuard)
    ) -> Any:
    """
    Get all lookup data.
    """
    access_token: str = auth.valid_token()
    if not access_token:
        raise InvalidTokenException()

    return await Controller().index(commons, request, auth.get_user())

@router.get("/{uid}",
        dependencies=[Depends(AuthGuard)],
        name="get_user",
        operation_id="get_user"
    )
async def show(
        uid: str,
        request: Request,
        auth: AuthGuard = Depends(AuthGuard)
    ) -> Any:
    """
    Get the user data with the given uid.
    """
    access_token: str = auth.valid_token()
    if not access_token:
        raise InvalidTokenException()

    return await Controller().show(uid, request, auth.get_user())

@router.post("/",
        dependencies=[Depends(AuthGuard)],
        name="create_user",
        operation_id="create_user"
    )
async def create(
        payload: UserCreateRequest,
        request: Request,
        auth: AuthGuard = Depends(AuthGuard)
    ) -> Any:
    """
    Create a new user with the given payload.
    """
    access_token: str = auth.valid_token()
    if not access_token:
        raise InvalidTokenException()

    return await Controller().create(
            payload, request,
            auth.get_user()
        )

@router.put("/{uid}",
        dependencies=[Depends(AuthGuard)],
        name="update_user",
        operation_id="update_user"
    )
async def update(
        uid: str,
        payload: UserUpdateRequest,
        request: Request,
        auth: AuthGuard = Depends(AuthGuard)
    ) -> Any:
    """
    Update the user with the given uid and payload.
    """
    return await Controller().update(
        uid, payload, request,
        auth.get_user()
    )

@router.delete("/{uid}",
        dependencies=[Depends(AuthGuard)],
        name="delete_user",
        operation_id="delete_user"
    )
async def delete(
        uid: str,
        request: Request,
        auth: AuthGuard = Depends(AuthGuard)
    ) -> Any:
    """
    Delete the user with the given uid.
    """
    return await Controller().delete(
        uid, request,
        auth.get_user()
    )
