""" Import the python standard libraries """
from typing import Annotated, Self

from pydantic import ConfigDict, Field

# Import the project models
from modules.base.models import (
    ApplicationBaseModel,
    AppBaseModelWithAuditLog
)

# Import the enums
from modules.core.enums.lookup import LookupMaster

class Lookup(AppBaseModelWithAuditLog):
    """
    Lookup model for the application.
    """
    lookup_key: str = Field(default=None, description="Name",
            max_length=128, examples=["my_lookup"]
        )
    display_value: str = Field(default=None, description="Value",
            max_length=128, examples=["My Lookup Value"]
        )
    description: str = Field(default=None, description="Description",
            exclude=False, max_length=256, examples=["My Lookup Description"]
        )

    lookup_type: LookupMaster = Field(default=None,
            description="Lookup Type",
            examples=["organization_type"]
        )

    order_by: int = Field(default=0, description="Order By",
            exclude=False, examples=[1]
        )
    is_editable: bool = Field(default=True, description="Is Editable",
            exclude=False, examples=[True]
        )

    model_config = ConfigDict(
        extra='forbid',
        populate_by_name=True,
        from_attributes=True
    )

class LookupMinor(ApplicationBaseModel):
    """
    Lookup model for the application.
    """
    lookup_key: str = Field(default=None, description="Name",
            max_length=128, examples=["my_lookup"]
        )
    display_value: str = Field(default=None, description="Value",
            max_length=128, examples=["My Lookup Value"]
        )
    lookup_type: LookupMaster = Field(default=None,
            description="Lookup Type",
            examples=["organization_type"]
        )

    model_config = ConfigDict(
        extra='forbid',
        populate_by_name=True,
        from_attributes=True
    )