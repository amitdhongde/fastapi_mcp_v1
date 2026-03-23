""" Import the required modules """
from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from modules.core.schemas import (
    OrganizationSchema,
    LookupSchema
)
from sqlalchemy import (
    Boolean,
    Integer,
    String,
    BigInteger,
    ForeignKey
)
from sqlalchemy.orm import (Mapped, mapped_column, relationship)

# Import Base Schema classes & models
from modules.base.db.base import (
    BaseDB,
    BaseSchemaUUIDAuditLogDeleteLog
)

# Import Enums
from modules.core.enums.lookup import LookupMaster

# Constants for foreign key references
ORGANIZATIONS_FK = 'organizations.id'
USERS_FK = 'users.id'
LOOKUPS_FK = 'lookups.id'

if TYPE_CHECKING:
    from modules.core.schemas import (
        LookupSchema,
        OrganizationSchema
    )

def relationship_back_populates_organization() -> OrganizationSchema:
    from modules.core.schemas import OrganizationSchema
    return OrganizationSchema

def relationship_back_populates_lookup() -> LookupSchema:
    from modules.core.schemas import LookupSchema
    return LookupSchema

class NoteSchema(BaseSchemaUUIDAuditLogDeleteLog, BaseDB):
    """
    Note model for the application.
    This model defines the structure of the note data.
    The base schema is inherited from BaseSchema_UUID_AuditLog_DeleteLog.
    This schema defines the structure of the base data. This schema
    includes the following fields:
    - id: Unique identifier for the note.
    
    """
    __tablename__ = "notes"

    # Foreign Key to References
    organization_id: Mapped[BigInteger] = mapped_column(
        ForeignKey(ORGANIZATIONS_FK), index=True
    )
    entity_type_id: Mapped[BigInteger] = mapped_column(
        ForeignKey(LOOKUPS_FK), nullable=False, index=True
    )
    reference_id: Mapped[BigInteger] = mapped_column(
        BigInteger, nullable=False, index=False
    )

    # Entity fields
    title: Mapped[str] = mapped_column(
        String(128), nullable=False
    )
    content: Mapped[Optional[str]] = mapped_column(
        String(8000), nullable=False
    )

    # Flags
    is_pinned: Mapped[bool] = mapped_column(Boolean, default=False)
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    organization: Mapped["OrganizationSchema"] = relationship(
            relationship_back_populates_organization,
            lazy="selectin",
            foreign_keys=[organization_id]
        )
    entity: Mapped["LookupSchema"] = relationship(
            relationship_back_populates_lookup,
            lazy="selectin",
            foreign_keys=[entity_type_id]
        )
