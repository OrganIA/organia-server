"""

Revision ID: 7721753e549f
Revises: c10e830b47cf
Create Date: 2022-07-18 02:17:10.228306

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7721753e549f'
down_revision = 'c10e830b47cf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('livers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('listing_id', sa.Integer(), nullable=True),
    sa.Column('tumors_number', sa.Integer(), nullable=False),
    sa.Column('biggest_tumor_size', sa.Integer(), nullable=True),
    sa.Column('alpha_fetoprotein', sa.Integer(), nullable=True),
    sa.Column('score', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['listing_id'], ['listings.id'], name=op.f('fk_livers_listing_id_listings')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_livers'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('livers')
    # ### end Alembic commands ###
