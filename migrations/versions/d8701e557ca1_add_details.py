"""add details

Revision ID: d8701e557ca1
Revises: ff4bc0ce7aa9
Create Date: 2024-10-29 16:38:44.604751

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd8701e557ca1'
down_revision: Union[str, None] = 'ff4bc0ce7aa9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todo', sa.Column('details', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('todo', 'details')
    # ### end Alembic commands ###
