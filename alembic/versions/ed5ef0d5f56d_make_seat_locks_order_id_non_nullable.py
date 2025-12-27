"""make seat_locks.order_id non-nullable

Revision ID: ed5ef0d5f56d
Revises: 7454e7024e4c
Create Date: 2025-12-27 21:50:31.972542

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


# revision identifiers, used by Alembic.
revision: str = 'ed5ef0d5f56d'
down_revision: Union[str, Sequence[str], None] = '7454e7024e4c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column(
        'seat_locks',
        'order_id',
        existing_type=mysql.INTEGER(),
        nullable=False
    )

def downgrade():
    op.alter_column(
        'seat_locks',
        'order_id',
        existing_type=mysql.INTEGER(),
        nullable=True
    )

# we are doing this in a separate migration to avoid issues with existing data