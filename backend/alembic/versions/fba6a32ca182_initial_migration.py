"""Initial migration

Revision ID: fba6a32ca182
Revises: 
Create Date: 2024-10-04 11:04:10.093732

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fba6a32ca182'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('employees',
    sa.Column('emp_code', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('street_address', sa.String(), nullable=False),
    sa.Column('town', sa.String(), nullable=False),
    sa.Column('zip', sa.String(), nullable=False),
    sa.Column('hire_date', sa.Date(), nullable=False),
    sa.Column('marital_status', sa.String(), nullable=False),
    sa.Column('comp_code', sa.String(), nullable=False),
    sa.Column('general_department', sa.String(), nullable=False),
    sa.Column('department', sa.String(), nullable=False),
    sa.Column('department_code', sa.String(), nullable=False),
    sa.Column('phone_number', sa.String(), nullable=False),
    sa.Column('hourly_salary', sa.String(), nullable=False),
    sa.Column('pay_type_code', sa.String(), nullable=False),
    sa.Column('date_of_birth', sa.Date(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('pay_rate', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('role', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('emp_code'),
    sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_employees_emp_code'), 'employees', ['emp_code'], unique=False)
    op.create_table('equipment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('equipment_number', sa.String(), nullable=False),
    sa.Column('equipment_name', sa.String(), nullable=False),
    sa.Column('equipment_type', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_equipment_id'), 'equipment', ['id'], unique=False)
    op.create_table('job_phases',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('job', sa.String(), nullable=False),
    sa.Column('phase_number', sa.String(), nullable=False),
    sa.Column('phase_name', sa.String(), nullable=True),
    sa.Column('cost_type', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_job_phases_id'), 'job_phases', ['id'], unique=False)
    op.create_index(op.f('ix_job_phases_job'), 'job_phases', ['job'], unique=False)
    op.create_index(op.f('ix_job_phases_phase_number'), 'job_phases', ['phase_number'], unique=False)
    op.create_table('timecards',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('emp_code', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('hours_worked', sa.Integer(), nullable=False),
    sa.Column('rate', sa.String(), nullable=False),
    sa.Column('extension', sa.String(), nullable=True),
    sa.Column('department', sa.String(), nullable=False),
    sa.Column('job', sa.String(), nullable=False),
    sa.Column('phase', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_timecards_id'), 'timecards', ['id'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('role', sa.Enum('mechanic', 'general', 'admin', name='userrole'), nullable=True),
    sa.Column('emp_code', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('bulk_receipt_uploads',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('admin_user_id', sa.Integer(), nullable=True),
    sa.Column('upload_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('file_name', sa.String(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('total_receipts', sa.Integer(), nullable=True),
    sa.Column('matched_receipts', sa.Integer(), nullable=True),
    sa.Column('unmatched_receipts', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['admin_user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_bulk_receipt_uploads_id'), 'bulk_receipt_uploads', ['id'], unique=False)
    op.create_table('daily_time_reports',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('hours_worked', sa.Integer(), nullable=True),
    sa.Column('job_name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('equipment', sa.String(), nullable=True),
    sa.Column('loads', sa.String(), nullable=True),
    sa.Column('pit', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_daily_time_reports_id'), 'daily_time_reports', ['id'], unique=False)
    op.create_index(op.f('ix_daily_time_reports_name'), 'daily_time_reports', ['name'], unique=False)
    op.create_table('mechanics_time_reports',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('hours_worked', sa.Integer(), nullable=True),
    sa.Column('equipment', sa.String(), nullable=True),
    sa.Column('equipment_number', sa.String(), nullable=True),
    sa.Column('cost_category', sa.String(), nullable=True),
    sa.Column('work_order_number', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_mechanics_time_reports_id'), 'mechanics_time_reports', ['id'], unique=False)
    op.create_index(op.f('ix_mechanics_time_reports_name'), 'mechanics_time_reports', ['name'], unique=False)
    op.create_table('credit_card_transactions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('emp_code', sa.String(length=10), nullable=False),
    sa.Column('card_last_four', sa.String(length=4), nullable=False),
    sa.Column('statement_date', sa.Date(), nullable=False),
    sa.Column('transaction_date', sa.Date(), nullable=False),
    sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('coding', sa.Text(), nullable=True),
    sa.Column('employee_coding', sa.Text(), nullable=True),
    sa.Column('image_path', sa.String(), nullable=True),
    sa.Column('bulk_upload_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['bulk_upload_id'], ['bulk_receipt_uploads.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_credit_card_transactions_id'), 'credit_card_transactions', ['id'], unique=False)
    op.create_table('receipts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('transaction_id', sa.Integer(), nullable=True),
    sa.Column('emp_code', sa.String(length=10), nullable=False),
    sa.Column('filename', sa.String(), nullable=True),
    sa.Column('upload_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('coding', sa.String(), nullable=True),
    sa.Column('employee_coding', sa.String(), nullable=True),
    sa.Column('image_path', sa.String(), nullable=True),
    sa.Column('bulk_upload_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['bulk_upload_id'], ['bulk_receipt_uploads.id'], ),
    sa.ForeignKeyConstraint(['transaction_id'], ['credit_card_transactions.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_receipts_filename'), 'receipts', ['filename'], unique=False)
    op.create_index(op.f('ix_receipts_id'), 'receipts', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_receipts_id'), table_name='receipts')
    op.drop_index(op.f('ix_receipts_filename'), table_name='receipts')
    op.drop_table('receipts')
    op.drop_index(op.f('ix_credit_card_transactions_id'), table_name='credit_card_transactions')
    op.drop_table('credit_card_transactions')
    op.drop_index(op.f('ix_mechanics_time_reports_name'), table_name='mechanics_time_reports')
    op.drop_index(op.f('ix_mechanics_time_reports_id'), table_name='mechanics_time_reports')
    op.drop_table('mechanics_time_reports')
    op.drop_index(op.f('ix_daily_time_reports_name'), table_name='daily_time_reports')
    op.drop_index(op.f('ix_daily_time_reports_id'), table_name='daily_time_reports')
    op.drop_table('daily_time_reports')
    op.drop_index(op.f('ix_bulk_receipt_uploads_id'), table_name='bulk_receipt_uploads')
    op.drop_table('bulk_receipt_uploads')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_timecards_id'), table_name='timecards')
    op.drop_table('timecards')
    op.drop_index(op.f('ix_job_phases_phase_number'), table_name='job_phases')
    op.drop_index(op.f('ix_job_phases_job'), table_name='job_phases')
    op.drop_index(op.f('ix_job_phases_id'), table_name='job_phases')
    op.drop_table('job_phases')
    op.drop_index(op.f('ix_equipment_id'), table_name='equipment')
    op.drop_table('equipment')
    op.drop_index(op.f('ix_employees_emp_code'), table_name='employees')
    op.drop_table('employees')
    # ### end Alembic commands ###
