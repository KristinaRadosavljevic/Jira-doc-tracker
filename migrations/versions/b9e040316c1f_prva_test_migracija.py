"""Prva test migracija

Revision ID: b9e040316c1f
Revises: 
Create Date: 2021-09-05 20:48:58.486251

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9e040316c1f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('nasa_tabela',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ime', sa.String(), nullable=True),
    sa.Column('godina', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('nasa_tabela')
    # ### end Alembic commands ###