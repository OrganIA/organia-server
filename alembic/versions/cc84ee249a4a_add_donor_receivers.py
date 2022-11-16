"""Add donor/receivers

Revision ID: cc84ee249a4a
Revises: 19d6140d7e2c
Create Date: 2021-06-11 01:33:48.723262

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc84ee249a4a'
down_revision = '19d6140d7e2c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('hospitals',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_hospitals'))
    )
    op.create_table('listings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('start_date', sa.Date(), nullable=True),
    sa.Column('end_date', sa.Date(), nullable=True),
    sa.Column('person_id', sa.Integer(), nullable=True),
    sa.Column('notes', sa.String(), nullable=True),
    sa.Column('hospital_id', sa.Integer(), nullable=True),
    sa.Column('donor', sa.Boolean(), nullable=False),
    sa.Column('organ', sa.Enum('HEART', name='organ'), nullable=True),
    sa.ForeignKeyConstraint(['hospital_id'], ['hospitals.id'], name=op.f('fk_listings_hospital_id_hospitals')),
    sa.ForeignKeyConstraint(['person_id'], ['persons.id'], name=op.f('fk_listings_person_id_persons')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_listings'))
    )
    op.create_table('staff',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('person_id', sa.Integer(), nullable=True),
    sa.Column('hospital_id', sa.Integer(), nullable=True),
    sa.Column('notes', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['hospital_id'], ['hospitals.id'], name=op.f('fk_staff_hospital_id_hospitals')),
    sa.ForeignKeyConstraint(['person_id'], ['persons.id'], name=op.f('fk_staff_person_id_persons')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_staff'))
    )
    with op.batch_alter_table('persons', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('gender', sa.Enum('MALE', 'FEMALE', 'OTHER', name='gender'), nullable=True))
        batch_op.add_column(sa.Column('abo', sa.Enum('A', 'B', 'AB', 'O', name='abo'), nullable=True))
        batch_op.add_column(sa.Column('rhesus', sa.Enum('POSITIVE', 'NEGATIVE', name='rhesus'), nullable=True))
        batch_op.create_unique_constraint(batch_op.f('uq_persons_user_id'), ['user_id'])
        # batch_op.drop_constraint('fk_persons_supervisor_id_users', type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('fk_persons_user_id_users'), 'users', ['user_id'], ['id'])
        batch_op.drop_column('supervisor_id')

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.VARCHAR(), nullable=False))

    with op.batch_alter_table('persons', schema=None) as batch_op:
        batch_op.add_column(sa.Column('supervisor_id', sa.INTEGER(), nullable=True))
        batch_op.drop_constraint(batch_op.f('fk_persons_user_id_users'), type_='foreignkey')
        batch_op.create_foreign_key('fk_persons_supervisor_id_users', 'users', ['supervisor_id'], ['id'])
        batch_op.drop_constraint(batch_op.f('uq_persons_user_id'), type_='unique')
        batch_op.drop_column('rhesus')
        batch_op.drop_column('abo')
        batch_op.drop_column('gender')
        batch_op.drop_column('user_id')

    op.drop_table('staff')
    op.drop_table('listings')
    op.drop_table('hospitals')
    # ### end Alembic commands ###