"""empty message

Revision ID: c7c7f561722c
Revises: 17a6e9bb787e
Create Date: 2018-04-14 04:23:19.198124

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7c7f561722c'
down_revision = '17a6e9bb787e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_order', sa.Column('is_see', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_order', 'is_see')
    # ### end Alembic commands ###
