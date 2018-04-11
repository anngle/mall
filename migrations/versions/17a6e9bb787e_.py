"""empty message

Revision ID: 17a6e9bb787e
Revises: 3a6a589ea412
Create Date: 2018-04-11 17:03:31.177047

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17a6e9bb787e'
down_revision = '3a6a589ea412'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_order', sa.Column('pay_type', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_order', 'pay_type')
    # ### end Alembic commands ###
