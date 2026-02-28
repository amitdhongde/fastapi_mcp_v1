# from fastapi import APIRouter, Depends
# from modules.base.exceptions.base import InvalidTokenException
# from modules.user.controllers.controller import UserController

# # Import middlewares
# from modules.base.fastapi.dependencies.authentication import AuthGaurd

# router = APIRouter(prefix="/users", tags=["Users"])

# @router.get("/", dependencies=[Depends(AuthGaurd)])
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

# @router.delete("/{hash}", dependencies=[Depends(AuthGaurd)])
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
from modules.base.fastapi.dependencies.authentication import AuthGaurd

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
            Depends(AuthGaurd),
            Depends(common_parameters)
        ],
        name="get_users",
        operation_id="get_user_list"
    )
async def index(
        commons: Annotated[dict, Depends(common_parameters)],
        request: Request,
        auth: AuthGaurd = Depends(AuthGaurd)
    ) -> Any:
    """
    Get all lookup data.
    """
    #current_user = auth.current_user()
    access_token: str = auth.valid_token()
    if not access_token:
        raise InvalidTokenException()

    current_user = {"id":1, "name":"test", "email":"amit@bond.ai"}
    return await Controller().index(commons, request, current_user)

@router.get("/{uid}",
        dependencies=[Depends(AuthGaurd)],
        name="get_user",
        operation_id="get_user"
    )
async def show(
        uid: str,
        request: Request,
        auth: AuthGaurd = Depends(AuthGaurd)
    ) -> Any:
    """
    Get the user data with the given uid.
    """
    #current_user = auth.current_user()
    access_token: str = auth.valid_token()
    if not access_token:
        raise

    current_user = {"id":1, "name":"test", "email":"amit@bond.ai"}
    return await Controller().show(uid, request, current_user)

@router.post("/",
        dependencies=[Depends(AuthGaurd)],
        name="create_user",
        operation_id="create_user"
    )
async def create(
        payload: UserCreateRequest,
        request: Request,
        auth: AuthGaurd = Depends(AuthGaurd)
    ) -> Any:
    """
    Create a new user with the given payload.
    """
    #current_user = auth.current_user()
    access_token: str = auth.valid_token()
    if not access_token:
        raise InvalidTokenException()

    current_user = {"id":1, "name":"test", "email":"amit@bond.ai"}

    return await Controller().create(
            payload, request,
            current_user
        )

@router.put("/{uid}",
        dependencies=[Depends(AuthGaurd)],
        name="update_user",
        operation_id="update_user"
    )
async def update(
        uid: str,
        payload: UserUpdateRequest,
        request: Request,
        auth: AuthGaurd = Depends(AuthGaurd)
    ) -> Any:
    """
    Update the user with the given uid and payload.
    """
    current_user = auth.current_user()
    return await Controller().update(
        uid, payload, request,
        current_user
    )

@router.delete("/{uid}",
        dependencies=[Depends(AuthGaurd)],
        name="delete_user",
        operation_id="delete_user"
    )
async def delete(
        uid: str,
        request: Request,
        auth: AuthGaurd = Depends(AuthGaurd)
    ) -> Any:
    """
    Delete the user with the given uid.
    """
    current_user = auth.current_user()
    return await Controller().delete(
        uid, request,
        current_user
    )
