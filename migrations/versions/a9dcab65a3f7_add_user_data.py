"""Add user data

Revision ID: a9dcab65a3f7
Revises: 14dcefe4cb9a
Create Date: 2026-02-24 10:50:20.949536

"""
import faker
import random
from typing import List, Sequence, Union

from alembic import op
import sqlalchemy as sa

from modules.base.config import config

# revision identifiers, used by Alembic.
revision: str = 'a9dcab65a3f7'
down_revision: Union[str, None] = '14dcefe4cb9a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Initialize Faker instance
fake = faker.Faker()

def upgrade() -> None:
    """Upgrade schema."""
    # Add key users as part of initial data setup for organizations
    # This is necessary to have at least one user associated with
    # the organization for admin and other operations
    user_data: List[dict] = []

    # Generate initial user data for the default organization
    user_data.append({
        'organization_id': 1,
        'type_id': 1,
        'first_name': 'Admin',
        'last_name': 'User',
        'is_pool': True,
    })

    # Generate initial user data only in non-production environments
    # to avoid inserting test data into production
    if config.ENVIRONMENT != 'production':
        # Generate initial user data
        for i in range(200):
            user_data.append({
                'organization_id': random.randint(1, 100),  # Assuming there are 100 organizations
                'type_id': 1,
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
            })

    user_table = sa.sql.table(
        'users',
        sa.sql.column('organization_id', sa.BigInteger),
        sa.sql.column('type_id', sa.BigInteger),
        sa.sql.column('first_name', sa.String),
        sa.sql.column('last_name', sa.String),
        sa.sql.column('is_pool', sa.Boolean)
    )
    op.bulk_insert(
        user_table,
        user_data,
        multiinsert=False
    )

def downgrade() -> None:
    """Downgrade schema."""
    pass
