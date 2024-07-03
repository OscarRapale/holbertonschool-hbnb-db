"""Second migration

Revision ID: b83cfdee6022
Revises: f38fa429f8cf
Create Date: 2024-07-03 12:49:59.902241

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b83cfdee6022'
down_revision: Union[str, None] = 'f38fa429f8cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
