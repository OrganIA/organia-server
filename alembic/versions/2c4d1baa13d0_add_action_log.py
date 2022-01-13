"""add action log

Revision ID: 2c4d1baa13d0
Revises: 6684f1a16849
Create Date: 2021-10-10 22:23:55.105814

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c4d1baa13d0'
down_revision = '6684f1a16849'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('action_logs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('action', sa.Enum('create', 'delete', 'edit', name='actiontype'), nullable=False),
    sa.Column('target_type', sa.String(), nullable=True),
    sa.Column('target_id', sa.Integer(), nullable=True),
    sa.Column('properties', sa.String(), nullable=True),
    sa.Column('message', sa.String(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], name=op.f('fk_action_logs_author_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_action_logs'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('action_logs')
    # ### end Alembic commands ###