"""

Revision ID: 573755749d15
Revises: f47913ab8ffa
Create Date: 2022-11-16 10:30:35.335214

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '573755749d15'
down_revision = 'f47913ab8ffa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('heart_scores', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sexR', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('ABO_R', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('MAL', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('MAL2', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('MAL3', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('DIA', sa.Boolean(), nullable=True))
        batch_op.drop_column('score')

    with op.batch_alter_table('livers', schema=None) as batch_op:
        batch_op.alter_column('tumors_number',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('livers', schema=None) as batch_op:
        batch_op.alter_column('tumors_number',
               existing_type=sa.INTEGER(),
               nullable=False)

    with op.batch_alter_table('heart_scores', schema=None) as batch_op:
        batch_op.add_column(sa.Column('score', sa.FLOAT(), nullable=True))
        batch_op.drop_column('DIA')
        batch_op.drop_column('MAL3')
        batch_op.drop_column('MAL2')
        batch_op.drop_column('MAL')
        batch_op.drop_column('ABO_R')
        batch_op.drop_column('sexR')

    # ### end Alembic commands ###