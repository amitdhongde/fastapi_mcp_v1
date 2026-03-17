from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional

# Importing necessary modules from SQLAlchemy
from sqlalchemy import (
    BigInteger,
    Integer,
    String,
    DateTime,
    Float,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import (relationship, Mapped, mapped_column)

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
    from modules.auth.schemas import AuthSchema

def relationship_back_populates_auth() -> AuthSchema:
    from modules.auth.schemas import AuthSchema
    return AuthSchema

def relationship_back_populates_organization() -> OrganizationSchema:
    from modules.core.schemas import OrganizationSchema
    return OrganizationSchema

def relationship_back_populates_lookup() -> LookupSchema:
    from modules.core.schemas import LookupSchema
    return LookupSchema

class UserSchema(BaseSchemaUUIDAuditLogDeleteLog, BaseDB):
    """
    User schema for serialization and validation.
    This schema defines the structure of the user data.
    """
    __tablename__ = 'users'

    # Foreign Key to References
    organization_id: Mapped[BigInteger] = mapped_column(
        ForeignKey(ORGANIZATIONS_FK), index=True
    )
    type_id: Mapped[BigInteger] = mapped_column(
        ForeignKey(LOOKUPS_FK), nullable=False, index=True
    )

    # User information
    title: Mapped[Optional[str]] = mapped_column(
        String(128), nullable=True
    )
    first_name: Mapped[str] = mapped_column(
        String(64), nullable=False
    )
    middle_name: Mapped[Optional[str]] = mapped_column(
        String(64), nullable=True
    )
    last_name: Mapped[Optional[str]] = mapped_column(
        String(64), nullable=True
    )
    avatar: Mapped[Optional[str]] = mapped_column(
        String(4000), nullable=True
    )

    date_of_birth: Mapped[Optional[DateTime]] = mapped_column(
        DateTime, nullable=True
    )
    gender_id: Mapped[BigInteger] = mapped_column(
        ForeignKey(LOOKUPS_FK), nullable=False
    )
    language_id: Mapped[BigInteger] = mapped_column(
        ForeignKey(LOOKUPS_FK), nullable=False
    )
    virtual_phone_number: Mapped[Optional[str]] = mapped_column(
        String(20), nullable=True
    )

    # Flags
    is_pool: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    # details: Mapped[List["UserDetailSchema"]] = relationship(
    #         "UserDetailSchema",
    #         lazy="joined",
    #         innerjoin=True,
    #         uselist=True
    #     )
    # addresses: Mapped[List["UserAddressSchema"]] = relationship(
    #         "UserAddressSchema",
    #         back_populates="user",
    #         lazy="joined"
    #     )
    organization: Mapped["OrganizationSchema"] = relationship(
            relationship_back_populates_organization,
            lazy="joined",
            foreign_keys=[organization_id]
        )
    type: Mapped[Optional["LookupSchema"]] = relationship(
            relationship_back_populates_lookup,
            lazy="joined",
            foreign_keys=[type_id]
        )
    gender: Mapped[Optional["LookupSchema"]] = relationship(
            relationship_back_populates_lookup,
            lazy="joined",
            foreign_keys=[gender_id]
        )
    # gender: Mapped[Optional["LookupSchema"]] = relationship(
        
    # )
    # authentications: Mapped[List["AuthSchema"]] = relationship(
    #     relationship_back_populates_auth,
    #     back_populates="user"
    # )

    def __repr__(self):
        return f"<UserSchema(id={self.id}, first_name={self.first_name})>"

class UserDetailSchema(BaseSchemaAuditLogDeleteLog, BaseDB):
    """
    User details schema for serialization and validation.
    This schema defines the structure of the user details data.
    """
    __tablename__ = 'user_details'

    # Foreign Key to References
    organization_id: Mapped[BigInteger] = mapped_column(
        ForeignKey(ORGANIZATIONS_FK), index=True
    )
    user_id: Mapped[BigInteger] = mapped_column(
        ForeignKey(USERS_FK), index=True
    )
    type_id: Mapped[BigInteger] = mapped_column(
        ForeignKey(LOOKUPS_FK), nullable=False, index=True
    )
    subtype_id: Mapped[Optional[BigInteger]] = mapped_column(
        ForeignKey(LOOKUPS_FK), nullable=True, index=True
    )

    # Entity information
    identifier: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    proxy: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )

    # Flags
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_secure: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    # user: Mapped["UserSchema"] = relationship(
    #         "UserSchema", 
    #         back_populates="details",
    #         uselist=False,
    #         lazy="joined"
    #     )

    def __repr__(self):
        return f"<UserDetailSchema(user_id={self.user_id}, identifier={self.identifier})>"

class UserAddressSchema(BaseSchemaAuditLogDeleteLog, BaseDB):
    """
    User address schema for serialization and validation.
    This schema defines the structure of the user address data.
    """
    __tablename__ = 'user_addresses'

    # Foreign Key to References
    organization_id: Mapped[BigInteger] = mapped_column(
        ForeignKey(ORGANIZATIONS_FK), index=True
    )
    user_id: Mapped[BigInteger] = mapped_column(
        ForeignKey(USERS_FK), index=True
    )
    type_id: Mapped[BigInteger] = mapped_column(
        ForeignKey(LOOKUPS_FK), nullable=False, index=True
    )

    # User information
    name: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    address_1: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    address_2: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    appartment_id: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True
    )
    society_id: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True
    )
    locality: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    city: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True
    )
    state: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True
    )
    country: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True
    )
    zipcode: Mapped[Optional[str]] = mapped_column(
        String(20), nullable=True
    )

    # Location information
    google_place_id: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    latitude: Mapped[Optional[float]] = mapped_column(
        Float(4), nullable=True
    )
    longitude: Mapped[Optional[float]] = mapped_column(
        Float(4), nullable=True
    )

    # Flags
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    # user: Mapped["UserSchema"] = relationship(
    #     "UserSchema", back_populates="addresses",
    #     uselist=False
    # )

    def __repr__(self):
        return f"<UserAddressSchema(user_id={self.user_id}, address_1={self.address_1})>"
