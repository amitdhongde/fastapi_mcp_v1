import functools
from typing import Any, Callable
from fastapi import Depends

# Include the project models
from modules.base.models.auth import AuthClaim
from modules.base.fastapi.dependencies.authentication import AuthGuard
from modules.base.exceptions import (
        ForbiddenException
    )

from .decorators import depends

def permissions(*allow_privileges: str) -> Callable[..., Any]:
    """
    Decorator to check permissions for a route.

    Args:
        permission (str): The permission to check.
        permission_type (str): The type of permission to check.
        is_admin_required (bool): Whether admin access is required.

    Returns:
        function: The decorated function.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @depends(_security_guard = Depends(AuthGuard))
        @functools.wraps(func)
        def wrapper(*args, _security_guard: AuthGuard, **kwargs) -> Any:
            # Get the claim from the guard
            claim: AuthClaim = _security_guard.get_claim()

            # Check permissions here
            if not {'any', 'all', '*'}.issuperset(set(allow_privileges)):

                # Get the privileges from the claim
                user_privileges: list[str] = claim.auth.get("privileges", [])

                # Check if user has any of the required privileges
                if not any(privilege in user_privileges for privilege in allow_privileges):
                    raise ForbiddenException("User does not have required privileges")

            return func(*args, **kwargs)
        return wrapper
    return decorator

def test_permissions(func: Callable) -> Callable:
    @functools.wraps(func)
    def test_func(*args, **kwargs):
        print("Testing permissions...")
        return func(*args, **kwargs)
    return test_func
