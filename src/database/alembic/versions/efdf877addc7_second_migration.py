"""Second Migration

Revision ID: efdf877addc7
Revises: 8f77c38ef2ad
Create Date: 2023-07-20 12:34:02.418048

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'efdf877addc7'
down_revision = '8f77c38ef2ad'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('CreditTransactions',
    sa.Column('ID', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('bad', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('ID', 'customer_id'),
    sa.UniqueConstraint('customer_id')
    )
    op.create_index(op.f('ix_CreditTransactions_ID'), 'CreditTransactions', ['ID'], unique=True)
    op.create_table('CustomerApplications',
    sa.Column('ID', sa.Integer(), nullable=False),
    sa.Column('email', sa.Integer(), nullable=False),
    sa.Column('annual_income', sa.Float(), nullable=False),
    sa.Column('total_children', sa.Integer(), nullable=True),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('has_realty', sa.Boolean(), nullable=True),
    sa.Column('has_car', sa.Boolean(), nullable=True),
    sa.Column('has_mobile_phone', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('ID'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_CustomerApplications_ID'), 'CustomerApplications', ['ID'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_CustomerApplications_ID'), table_name='CustomerApplications')
    op.drop_table('CustomerApplications')
    op.drop_index(op.f('ix_CreditTransactions_ID'), table_name='CreditTransactions')
    op.drop_table('CreditTransactions')
    # ### end Alembic commands ###
