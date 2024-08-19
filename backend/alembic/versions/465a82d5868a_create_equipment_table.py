"""Create equipment table

Revision ID: 465a82d5868a
Revises: 22d27e6e9750
Create Date: 2024-08-18 19:52:34.182369

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '465a82d5868a'
down_revision: Union[str, None] = '22d27e6e9750'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('jobs')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('jobs',
    sa.Column('job', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('phase_number', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('phase_name', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('cost_type', sa.TEXT(), autoincrement=False, nullable=True)
    )
    # ### end Alembic commands ###
