""" Import the required modules """
from __future__ import annotations
import datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy import (
    DateTime,
    Boolean,
    Integer,
    String,
    BigInteger,
    ForeignKey
)
from sqlalchemy.orm import (Mapped, mapped_column, relationship)

# Import Base Schema classes & models
from modules.base.db import (
    BaseDB,
    BaseSchemaAuditLogDeleteLog,
    BaseSchemaUUIDAuditLogDeleteLog
)


# Constants for foreign key references
ORGANIZATIONS_FK = 'organizations.id'
USERS_FK = 'users.id'
LOOKUPS_FK = 'lookups.id'

if TYPE_CHECKING:
    from modules.core.schemas import (
        LookupSchema,
        OrganizationSchema
    )
    from modules.user.schemas import UserSchema

def relationship_back_populates_user() -> UserSchema:
    from modules.user.schemas import UserSchema
    return UserSchema

def relationship_back_populates_organization() -> OrganizationSchema:
    from modules.core.schemas import OrganizationSchema
    return OrganizationSchema

def relationship_back_populates_lookup() -> LookupSchema:
    from modules.core.schemas import LookupSchema
    return LookupSchema
    

class AuthSchema(BaseSchemaUUIDAuditLogDeleteLog, BaseDB):
    """
    Authentication model for the application.

    This model defines the structure of the authentication data.
    The base schema is inherited from BaseSchema_UUID_AuditLog_DeleteLog.
    This schema defines the structure of the base data. This schema
    includes the following fields:

    - id: Unique identifier for the authentication record.
    
    """
    __tablename__ = "authentications"

    # Foreign fields
    organization_id: Mapped[int] = mapped_column(ForeignKey(ORGANIZATIONS_FK), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(USERS_FK), index=True)
    type_id: Mapped[int] = mapped_column(ForeignKey(LOOKUPS_FK), index=True)

    # Entity fields
    sub: Mapped[Optional[str]] = mapped_column(String(255), nullable=True,
            unique=True, index=True
        )
    username: Mapped[str] = mapped_column(String(64), nullable=False,
            unique=True, index=True
        )
    password: Mapped[str] = mapped_column(String(255), nullable=True)
    remember_token: Mapped[bool] = mapped_column(Boolean, default=False)
    remember_expire_at: Mapped[Optional[datetime.datetime]] = mapped_column(
            DateTime(timezone=True), nullable=True,
        )
    last_login_at: Mapped[Optional[datetime.datetime]] = mapped_column(
            DateTime(timezone=True), nullable=True,
        )
    last_login_ip: Mapped[Optional[str]] = mapped_column(
            String(45), nullable=True
        )

    # Flags
    is_agent: Mapped[bool] = mapped_column(Boolean, default=False)
    is_remote_access_only: Mapped[bool] = mapped_column(Boolean, default=False)
    failed_attempts: Mapped[int] = mapped_column(Integer, default=0)
    max_failed_attempts: Mapped[int] = mapped_column(Integer, default=5)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    verification_token: Mapped[Optional[str]] = mapped_column(
            String(255), nullable=True
        )
    verification_token_expires_at: Mapped[Optional[datetime.datetime]] = mapped_column(
            DateTime(timezone=True), nullable=True,
        )
    verified_at: Mapped[Optional[datetime.datetime]] = mapped_column(
            DateTime(timezone=True), nullable=True,
        )

    # Relationships
    # organization: Mapped["OrganizationSchema"] = relationship(
    #         relationship_back_populates_organization,
    #         foreign_keys=[organization_id],
    #         lazy="select"
    #     )
    # type: Mapped["LookupSchema"] = relationship(
    #         relationship_back_populates_lookup,
    #         foreign_keys=[type_id]
    #     )
    # user: Mapped["UserSchema"] = relationship(
    #         relationship_back_populates_user,
    #         foreign_keys=[user_id]
    #     )

class RegistrationSchema(BaseSchemaAuditLogDeleteLog, BaseDB):
    """
    Registration model for the application.

    This model defines the structure of the registration data.
    The base schema is inherited from BaseSchema_UUID_AuditLog_DeleteLog.
    This schema defines the structure of the base data. This schema
    includes the following fields:
    - id: Unique identifier for the registration.
    
    """
    __tablename__ = "registrations"

    # Entity fields
    first_name: Mapped[str] = mapped_column(
        String(64), nullable=False
    )
    middle_name: Mapped[Optional[str]] = mapped_column(
        String(64), nullable=True
    )
    last_name: Mapped[str] = mapped_column(
        String(64), nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(128), nullable=False,
        index=True
    )
    phone: Mapped[Optional[str]] = mapped_column(
        String(20), nullable=True
    )
