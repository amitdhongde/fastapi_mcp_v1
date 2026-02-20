"""Add document table

Revision ID: 7136741bac89
Revises: 8ed5c1291495
Create Date: 2026-02-20 17:10:10.325083

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7136741bac89'
down_revision: Union[str, None] = '8ed5c1291495'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
