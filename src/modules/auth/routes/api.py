""" Import the required modules """
from typing import Any, Annotated
from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm

# Import middlewares and dependencies
from modules.base.fastapi.dependencies.authentication import (
        AuthGuard,
        get_auth_guard
    )
from modules.base.fastapi.decorations import permissions
from modules.base.exceptions import (
        AuthenticationException,
        ModelValidationException
    )

# Include the project controllers
from modules.auth.controllers import AuthController as Controller

# Include the project models
from modules.auth.models.request import (
        LoginRequest,
        RegisterRequest,
        ForgotPasswordRequest,
        ChangePasswordRequest
    )

# Create the module router
router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/token")
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        request: Request = Depends(Request),
        controller: Controller = Depends()
    ) -> Any:
    """ 
    Authenticate the user and return an access token by converting
    the OAuth2PasswordRequestForm to a LoginRequest.
    """
    try:
        payload: LoginRequest = LoginRequest(
            username=form_data.username,
            code=form_data.password
        )
        return await controller.authenticate(payload, request)
    except AuthenticationException as e:
        raise e
    except Exception as e:
        raise ModelValidationException(e) from e

@router.post("/login")
async def authenticate(
        credentials: LoginRequest,
        request: Request,
        controller: Controller = Depends()
    ) -> Any:
    """
    Authenticate a user with the given credentials.
    """
    return await controller.authenticate(credentials, request)

@router.put("/logout",
        dependencies=[Depends(get_auth_guard)]
    )
@permissions("*")
async def logout(
        guard: Annotated[AuthGuard, Depends(get_auth_guard)],
        controller: Controller = Depends()
    ) -> Any:
    """
    Logout a user with the given access token.
    """
    access_token: str = guard.get_token()
    return await controller.logout(access_token, is_forced=False)

@router.put("/logout/forced",
        dependencies=[Depends(get_auth_guard)],
        name="forced_logout"
    )
@permissions("*")
async def logout_forced(
    guard: Annotated[AuthGuard, Depends(get_auth_guard)],
    controller: Controller = Depends()
    ) -> Any:
    """
    Logout a user with the given access token for all devices.
    This is a forced logout.
    """
    access_token: str = guard.get_token()
    return await controller.logout(access_token, is_forced=True)

@router.post("/register")
async def register(
        payload: RegisterRequest,
        request: Request,
        controller: Controller = Depends()
    ) -> Any:
    """
    Register a new user with the given payload.
    """
    return await controller.register(payload, request)

@router.post("/forgot-password")
async def forgot_password(
        payload: ForgotPasswordRequest,
        request: Request = Depends(Request),
        controller: Controller = Depends()
    ) -> Any:
    """
    Send a forgot password email to the user with the given payload.
    """
    return await controller.forgot_password(payload, request)

@router.post("/change-password", dependencies=[Depends(get_auth_guard)])
async def change_password(
        payload: ChangePasswordRequest,
        guard: Annotated[AuthGuard, Depends(get_auth_guard)],
        request: Request = Depends(Request),
        controller: Controller = Depends()
    ) -> Any:
    """
    Change the password of the user with the given payload.
    """
    return await controller.change_password(payload, request)

@router.get("/token/refresh",
        dependencies=[Depends(get_auth_guard)],
        name="refresh_token"
    )
async def refresh_token(
        guard: Annotated[AuthGuard, Depends(get_auth_guard)],
        request: Request = Depends(Request),
        controller: Controller = Depends()
    ) -> Any:
    """
    Refresh the access token of the user with the given refresh token.
    """
    access_token: str = guard.get_token()
    return await controller.refresh_token(access_token, request)
