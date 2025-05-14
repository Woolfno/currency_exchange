"""id set default gen_random_uuid()

Revision ID: 8d881ef418c3
Revises: 502c5f0d0ad1
Create Date: 2025-03-24 23:16:35.968490

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8d881ef418c3'
down_revision: Union[str, None] = '502c5f0d0ad1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
