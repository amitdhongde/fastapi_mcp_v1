""" Import the python standard libraries """
from pydantic import Field

# Import the project models
from modules.base.models import AppBaseModelWithHashAndAuditLog

class Organization(AppBaseModelWithHashAndAuditLog):
    """
    Organization model for the application.
    """
    display_name: str = Field(default=None, description="Display Name",
            max_length=128, examples=["My Organization"]
        )
    legal_name: str = Field(default=None, description="Legal Name",
            exclude=True, max_length=128,
            examples=["My Organization Inc"]
        )

class OrganizationMinor(Organization):
    """
    Organization Minor model for the application.
    This model is used for the minor details of the organization.
    """
    id: int = Field(exclude=True)
