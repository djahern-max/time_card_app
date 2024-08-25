"""Add emp_code to receipts

Revision ID: 287d37eaa7be
Revises: 3fac4a9736f6
Create Date: 2024-08-25 10:29:12.303435

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '287d37eaa7be'
down_revision: Union[str, None] = '3fac4a9736f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('receipts', sa.Column('emp_code', sa.String(length=10), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('receipts', 'emp_code')
    # ### end Alembic commands ###
