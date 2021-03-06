"""empty message

Revision ID: 24c90d243db8
Revises: 4e15ac65dd94
Create Date: 2018-03-17 17:44:26.343605

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '24c90d243db8'
down_revision = '4e15ac65dd94'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('inventory', sa.Column('note', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('inventory', 'note')
    # ### end Alembic commands ###
