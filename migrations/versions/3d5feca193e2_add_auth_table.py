"""Add auth table

Revision ID: 3d5feca193e2
Revises: 4510d233ebde
Create Date: 2026-02-24 12:16:23.919188

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3d5feca193e2'
down_revision: Union[str, None] = '4510d233ebde'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'authentications',
        sa.Column('id', sa.BigInteger(),
            autoincrement=True, nullable=False,
            primary_key=True, index=True
        ),
        sa.Column('hash', sa.String(length=36),
            server_default=sa.text('UUID()'),
            unique=True, index=True,
            nullable=False
        ),
        sa.Column('organization_id', sa.BigInteger(),
            server_default=sa.text('0'),
            nullable=False, index=True
        ),
        sa.Column('user_id', sa.BigInteger(),
            server_default=sa.text('0'),
            nullable=False, index=True
        ),
        sa.Column('type_id', sa.BigInteger(),
            server_default=sa.text('0'),
            nullable=False, index=True
        ),
        sa.Column('sub', sa.String(length=255),
            nullable=True, unique=True, index=True
        ),
        sa.Column('username', sa.String(length=64),
            nullable=False, unique=True, index=True
        ),
        sa.Column('password', sa.String(length=255),
            nullable=True
        ),
        sa.Column('remember_token', sa.Boolean(),
            server_default=sa.text('0'),
            nullable=False
        ),
        sa.Column('remember_expire_at', sa.DateTime(timezone=True),
            nullable=True
        ),
        sa.Column('last_login_at', sa.DateTime(timezone=True),
            nullable=True
        ),
        sa.Column('last_login_ip', sa.String(length=255),
            nullable=True
        ),
        sa.Column('is_agent', sa.Boolean(),
            server_default=sa.text('0'),
            nullable=False
        ),
        sa.Column('is_remote_access_only', sa.Boolean(),
            server_default=sa.text('0'),
            nullable=False
        ),
        sa.Column('failed_attempts', sa.Integer(),
            server_default=sa.text('0'),
            nullable=False
        ),
        sa.Column('max_failed_attempts', sa.Integer(),
            server_default=sa.text('5'),
            nullable=False
        ),
        sa.Column('is_verified', sa.Boolean(),
            server_default=sa.text('0'),
            nullable=False
        ),
        sa.Column('verification_token', sa.String(length=255),
            nullable=True
        ),
        sa.Column('verification_token_expires_at', sa.DateTime(timezone=True),
            nullable=True
        ),
        sa.Column('verified_at', sa.DateTime(timezone=True),
            nullable=True
        ),
        sa.Column('created_at', sa.DateTime(timezone=True),
            server_default=sa.text('UTC_TIMESTAMP()'),
            nullable=False
        ),
        sa.Column('created_by', sa.BigInteger(),
            server_default=sa.text('0'),
            nullable=False
        ),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_by', sa.BigInteger(), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('deleted_by', sa.BigInteger(), nullable=True),
        sa.Column('is_active', sa.Boolean(),
            server_default=sa.text('1'),
            nullable=False
        ),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ),
        sa.PrimaryKeyConstraint('id'),
        if_not_exists=True
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_auth_sub'), table_name='authentications')
    op.drop_index(op.f('ix_auth_username'), table_name='authentications')
    op.drop_index(op.f('ix_auth_organization_id'), table_name='authentications')
    op.drop_index(op.f('ix_auth_user_id'), table_name='authentications')
    op.drop_index(op.f('ix_auth_type_id'), table_name='authentications')
    op.drop_index(op.f('ix_auth_hash'), table_name='authentications')
    op.drop_index(op.f('ix_auth_id'), table_name='authentications')
    op.drop_table('authentications')
    # ### end Alembic commands ###