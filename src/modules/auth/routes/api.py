""" Import the required modules """
from typing import Any, Annotated
from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm

# Import middlewares and dependencies
from modules.base.fastapi.dependencies.authentication import AuthGaurd, get_auth_token
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
        request: Request,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
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
        dependencies=[Depends(AuthGaurd), Depends(get_auth_token)]
    )
@permissions("*")
async def logout(
        token: Annotated[str, Depends(get_auth_token)],
        controller: Controller = Depends()
    ) -> Any:
    """
    Logout a user with the given access token.
    """
    access_token: str = token
    return await controller.logout(access_token, is_forced=False)

@router.put("/logout/forced",
        dependencies=[Depends(AuthGaurd)],
        name="forced_logout"
    )
@permissions("*")
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
