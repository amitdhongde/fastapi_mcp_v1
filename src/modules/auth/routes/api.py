""" Import the required modules """
from typing import Any
from fastapi import APIRouter, Depends, Request

# Import middlewares and dependencies
from modules.base.fastapi.dependencies.authentication import AuthGaurd

# Include the project controllers
from ..controllers import AuthController as Controller

# Include the project models
from ..models.request import (
    LoginRequest,
    RegisterRequest,
    ForgotPasswordRequest,
    ChangePasswordRequest
)

# Create the module router
router = APIRouter(prefix="/auth", tags=["Authentication"])

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
        dependencies=[Depends(AuthGaurd)]
    )
async def logout(
        auth: AuthGaurd = Depends(AuthGaurd),
        controller: Controller = Depends()
    ) -> Any:
    """
    Logout a user with the given access token.
    """
    access_token: str = auth.valid_token()
    return await controller.logout(access_token, is_forced=False)


@router.put("/logout/forced",
        dependencies=[Depends(AuthGaurd)],
        name="forced_logout"
    )
async def logout_forced(
    auth: AuthGaurd = Depends(AuthGaurd),
    controller: Controller = Depends()
    ) -> Any:
    """
    Logout a user with the given access token for all devices.
    This is a forced logout.
    """
    access_token: str = auth.valid_token()
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
        request: Request,
        controller: Controller = Depends()
    ) -> Any:
    """
    Send a forgot password email to the user with the given payload.
    """
    return await controller.forgot_password(payload, request)


@router.post("/change-password", dependencies=[Depends(AuthGaurd)])
async def change_password(
        payload: ChangePasswordRequest,
        request: Request,
        auth: AuthGaurd = Depends(AuthGaurd),
        controller: Controller = Depends()
    ) -> Any:
    """
    Change the password of the user with the given payload.
    """
    return await controller.change_password(payload, request)


@router.get("/token/refresh",
        dependencies=[Depends(AuthGaurd)],
        name="refresh_token"
    )
async def refresh_token(
        request: Request,
        auth: AuthGaurd = Depends(AuthGaurd),
        controller: Controller = Depends()
    ) -> Any:
    """
    Refresh the access token of the user with the given refresh token.
    """
    access_token: str = auth.valid_token()
    return await controller.refresh_token(access_token, request)
