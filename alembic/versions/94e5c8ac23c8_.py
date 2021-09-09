"""

Revision ID: 94e5c8ac23c8
Revises: c362bbe9eef1
Create Date: 2021-09-09 21:08:55.762384

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94e5c8ac23c8'
down_revision = 'c362bbe9eef1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('roles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(), nullable=False))
        batch_op.create_unique_constraint(batch_op.f('uq_roles_name'), ['name'])

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_users_role_id'), ['role_id'])
        batch_op.create_foreign_key(batch_op.f('fk_users_role_id_roles'), 'roles', ['role_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_users_role_id_roles'), type_='foreignkey')
        batch_op.drop_constraint(batch_op.f('uq_users_role_id'), type_='unique')

    with op.batch_alter_table('roles', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_roles_name'), type_='unique')
        batch_op.drop_column('name')

    # ### end Alembic commands ###
