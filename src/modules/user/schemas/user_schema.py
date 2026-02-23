from typing import Optional

from sqlalchemy import (
    BigInteger,
    Column,
    Double,
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

class UserSchema(BaseSchemaUUIDAuditLogDeleteLog, BaseDB):
    """
    User schema for serialization and validation.
    This schema defines the structure of the user data.
    """
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    # Foreign Key to References
    organization_id: Mapped[BigInteger] = mapped_column(
        ForeignKey(ORGANIZATIONS_FK), index=True
    )
    type_id: Mapped[Optional[BigInteger]] = mapped_column(
        ForeignKey(LOOKUPS_FK), nullable=True, index=True
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
    gender_id: Mapped[Optional[BigInteger]] = mapped_column(
        ForeignKey(LOOKUPS_FK), nullable=True, index=True
    )
    language_id: Mapped[Optional[BigInteger]] = mapped_column(
        ForeignKey(LOOKUPS_FK), nullable=True, index=True
    )
    virtual_phone_number: Mapped[Optional[str]] = mapped_column(
        String(20), nullable=True
    )

    # Flags
    is_pool: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    details: Mapped["UserDetailSchema"] = relationship(
        "UserDetailSchema", back_populates="user",
        uselist=False, cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<UserSchema(id={self.id}, username={self.username}, email={self.email})>"

class UserDetailSchema(BaseSchemaAuditLogDeleteLog, BaseDB):
    """
    User details schema for serialization and validation.
    This schema defines the structure of the user details data.
    """
    __tablename__ = 'user_details'
    __table_args__ = {'extend_existing': True}

    # Foreign Key to References
    organization_id = Column(BigInteger, ForeignKey(ORGANIZATIONS_FK),
        nullable=False, index=True
    )
    user_id = Column(BigInteger, ForeignKey(USERS_FK),
        nullable=False, index=True
    )
    type_id = Column(BigInteger, ForeignKey(LOOKUPS_FK),
        nullable=True, index=True
    )
    subtype_id = Column(BigInteger, ForeignKey(LOOKUPS_FK),
        nullable=True, index=True
    )

    # Entity information
    identifier = Column(String(255), nullable=True)
    proxy = Column(String(255), nullable=True)

    # Flags
    is_primary = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)

    # Relationships
    user: Mapped["UserSchema"] = relationship(
        "UserSchema", back_populates="details",
        uselist=False, cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<UserDetailSchema(user_id={self.user_id}, identifier={self.identifier})>"

class UserAddress(BaseSchemaAuditLogDeleteLog, BaseDB):
    """
    User address schema for serialization and validation.
    This schema defines the structure of the user address data.
    """
    __tablename__ = 'user_addresses'
    __table_args__ = {'extend_existing': True}

    # Foreign Key to References
    organization_id = Column(BigInteger, ForeignKey(ORGANIZATIONS_FK),
        nullable=False, index=True
    )
    user_id = Column(BigInteger, ForeignKey(USERS_FK),
        nullable=False, index=True
    )
    type_id = Column(BigInteger, ForeignKey(LOOKUPS_FK),
        nullable=True, index=True
    )

    # User information
    name = Column(String(255), nullable=True)
    address_1 = Column(String(255), nullable=True)
    address_2 = Column(String(255), nullable=True)
    appartment_id = Column(Integer, nullable=True)
    society_id = Column(Integer, nullable=True)
    locality = Column(String(255), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    zipcode = Column(String(20), nullable=True)

    # Location information
    google_place_id = Column(String(255), nullable=True)
    latitude = Column(Float(4), nullable=True)
    longitude = Column(Float(4), nullable=True)

    # Flags
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    user: Mapped["UserSchema"] = relationship(
        "UserSchema", back_populates="addresses",
        uselist=False, cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<UserAddress(user_id={self.user_id}, address_1={self.address_1})>"
