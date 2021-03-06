"""empty message

Revision ID: 220cd2617379
Revises: 7baf280f330a
Create Date: 2018-03-17 02:08:16.137713

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '220cd2617379'
down_revision = '7baf280f330a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('goodsed', sa.Column('attach_key', sa.String(length=500), nullable=True))
    op.add_column('goodsed', sa.Column('attach_value', sa.String(length=500), nullable=True))
    op.add_column('receipts', sa.Column('goods_sum', sa.Integer(), nullable=True))
    op.add_column('receipts', sa.Column('price_sum', sa.Numeric(precision=15, scale=2), nullable=True))
    op.add_column('receipts', sa.Column('variety', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('receipts', 'variety')
    op.drop_column('receipts', 'price_sum')
    op.drop_column('receipts', 'goods_sum')
    op.drop_column('goodsed', 'attach_value')
    op.drop_column('goodsed', 'attach_key')
    # ### end Alembic commands ###
