"""Add note data

Revision ID: 4510d233ebde
Revises: a9dcab65a3f7
Create Date: 2026-02-24 10:51:27.023843

"""
import faker
import random
from typing import List, Sequence, Union

from alembic import op
import sqlalchemy as sa

from modules.base.config import config

# revision identifiers, used by Alembic.
revision: str = '4510d233ebde'
down_revision: Union[str, None] = 'a9dcab65a3f7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Initialize Faker instance
fake = faker.Faker()

def upgrade() -> None:
    """Upgrade schema."""
    # Generate initial note data only in non-production environments
    # to avoid inserting test data into production
    if config.ENVIRONMENT == 'production':
        return  # Skip data insertion in production environment

    note_data: List[dict] = []
    
    # Generate initial note data
    for i in range(100):
        note_data.append({
            'organization_id': 1,
            'entity_type_id': 1,
            'reference_id': 1,
            'title': fake.sentence(nb_words=6),
            'content': fake.paragraph(nb_sentences=3),
            'is_pinned': random.choice([True, False]),
            'is_archived': random.choice([True, False])
        })

    note_table = sa.sql.table(
        'notes',
        sa.sql.column('organization_id', sa.BigInteger),
        sa.sql.column('entity_type_id', sa.BigInteger),
        sa.sql.column('reference_id', sa.BigInteger),
        sa.sql.column('title', sa.String),
        sa.sql.column('content', sa.String),
        sa.sql.column('is_pinned', sa.Boolean),
        sa.sql.column('is_archived', sa.Boolean)
    )

    op.bulk_insert(
        note_table,
        note_data,
        multiinsert=False
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
