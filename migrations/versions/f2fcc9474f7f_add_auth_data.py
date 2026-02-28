"""Add auth data

Revision ID: f2fcc9474f7f
Revises: 3d5feca193e2
Create Date: 2026-02-24 12:16:33.496495

"""
import faker
import random
from typing import List, Sequence, Union

from alembic import op
import sqlalchemy as sa

from modules.base.config import config


# revision identifiers, used by Alembic.
revision: str = 'f2fcc9474f7f'
down_revision: Union[str, None] = '3d5feca193e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Initialize Faker instance
fake = faker.Faker()

def upgrade() -> None:
    """Upgrade schema."""
    # Add key user auth data as part of initial data setup for organizations
    # This is necessary to have at least one auth record associated with
    # the user for admin and other operations
    auth_data: List[dict] = []
    # Generate initial auth data for the default user
    auth_data.append({
        "organization_id": 1,
        "user_id": 1,
        "type_id": 1,
        "sub": fake.uuid4(),
        "username": 'admin@domain.com',
        "password": fake.password(length=12),
        "remember_token": False,
        "is_agent": False,
        "is_remote_access_only": False,
        "failed_attempts": 0,
        "max_failed_attempts": 5,
        "is_verified": True,
    })

    # Generate initial auth data only in non-production environments
    # to avoid inserting test data into production
    if config.ENVIRONMENT != 'production':
        # Generate initial auth data
        for i in range(200):
            auth_data.append({
                "organization_id": random.randint(1, 100),  # Assuming there are 100 organizations
                "user_id": random.randint(1, 200),  # Assuming there are 200 users
                "type_id": 1,
                "sub": fake.uuid4(),
                "username": fake.user_name(),
                "password": fake.password(length=12),
                "remember_token": False,
                "is_agent": False,
                "is_remote_access_only": False,
                "failed_attempts": 0,
                "max_failed_attempts": 5,
                "is_verified": True,
            })
    # Insert auth data into the auth table
    auth_table = sa.sql.table(
        'authentications',
        sa.sql.column('organization_id', sa.BigInteger),
        sa.sql.column('user_id', sa.BigInteger),
        sa.sql.column('type_id', sa.BigInteger),
        sa.sql.column('sub', sa.String),
        sa.sql.column('username', sa.String),
        sa.sql.column('password', sa.String),
        sa.sql.column('remember_token', sa.Boolean),
        sa.sql.column('is_agent', sa.Boolean),
        sa.sql.column('is_remote_access_only', sa.Boolean),
        sa.sql.column('failed_attempts', sa.Integer),
        sa.sql.column('max_failed_attempts', sa.Integer),
        sa.sql.column('is_verified', sa.Boolean)
    )
    op.bulk_insert(auth_table, auth_data, multiinsert=False)

def downgrade() -> None:
    """Downgrade schema."""
    pass
