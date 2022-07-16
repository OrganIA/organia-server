"""add firstname lastname and phone number to users

Revision ID: d59b3e678183
Revises: c10e830b47cf
Create Date: 2022-07-05 16:41:37.629734

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd59b3e678183'
down_revision = 'c10e830b47cf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('firstname', sa.String(), nullable=False))
        batch_op.add_column(sa.Column('lastname', sa.String(), nullable=False))
        batch_op.add_column(sa.Column('phone_number', sa.Unicode(length=20), nullable=True))
        batch_op.add_column(sa.Column('country_code', sa.Unicode(length=8), nullable=True))
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.drop_column('country_code')
        batch_op.drop_column('phone_number')
        batch_op.drop_column('lastname')
        batch_op.drop_column('firstname')

    # ### end Alembic commands ###
