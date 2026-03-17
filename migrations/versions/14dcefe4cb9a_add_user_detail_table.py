"""Add user_detail table

Revision ID: 14dcefe4cb9a
Revises: fddfdfe7300d
Create Date: 2026-02-23 23:36:52.955430

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '14dcefe4cb9a'
down_revision: Union[str, None] = 'fddfdfe7300d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('user_details',
        sa.Column('id', sa.BigInteger(),
            autoincrement=True, nullable=False,
            primary_key=True, index=True
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
        sa.Column('subtype_id', sa.BigInteger(),
            server_default=sa.text('0'),
            nullable=True
        ),
        sa.Column('identifier', sa.String(length=255),
            nullable=True
        ),
        sa.Column('proxy', sa.String(length=255),
            nullable=True
        ),
        sa.Column('is_primary', sa.Boolean(),
            server_default=sa.text('0'),
            nullable=False
        ),
        sa.Column('is_verified', sa.Boolean(),
            server_default=sa.text('0'),
            nullable=False
        ),
        sa.Column('is_secure', sa.Boolean(),
            server_default=sa.text('0'),
            nullable=False
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
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_user_details_organization_id'), table_name='user_details')
    op.drop_index(op.f('ix_user_details_user_id'), table_name='user_details')
    op.drop_index(op.f('ix_user_details_type_id'), table_name='user_details')
    op.drop_index(op.f('ix_user_details_subtype_id'), table_name='user_details')
    op.drop_index(op.f('ix_user_details_id'), table_name='user_details')
    op.drop_table('user_details')
