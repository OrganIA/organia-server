"""Add calendar events

Revision ID: c564a4809a7d
Revises: 2c4d1baa13d0
Create Date: 2021-12-06 20:00:00.578492

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c564a4809a7d'
down_revision = '2c4d1baa13d0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('calendar_events',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], name=op.f('fk_calendar_events_author_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_calendar_events'))
    )
    with op.batch_alter_table('hospitals', schema=None) as batch_op:
        batch_op.create_foreign_key(batch_op.f('fk_hospitals_city_id_cities'), 'cities', ['city_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('hospitals', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_hospitals_city_id_cities'), type_='foreignkey')

    op.drop_table('calendar_events')
    # ### end Alembic commands ###