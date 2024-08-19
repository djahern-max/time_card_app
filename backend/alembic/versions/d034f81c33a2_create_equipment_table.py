"""Create equipment table

Revision ID: d034f81c33a2
Revises: 465a82d5868a
Create Date: 2024-08-18 20:05:51.192748

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd034f81c33a2'
down_revision: Union[str, None] = '465a82d5868a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('equipment',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('equipment_number', sa.String(), nullable=False),
        sa.Column('equipment_name', sa.String(), nullable=False),
        sa.Column('equipment_type', sa.String(), nullable=False),
        
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_equipment_equipment_number'), 'equipment', ['equipment_number'], unique=False)
    op.create_index(op.f('ix_equipment_id'), 'equipment', ['id'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_equipment_id'), table_name='equipment')
    op.drop_index(op.f('ix_equipment_equipment_number'), table_name='equipment')
    op.drop_table('equipment')
