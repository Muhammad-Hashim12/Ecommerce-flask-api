""" removed forign keyfrom payments of orderid 

Revision ID: fd171ad09978
Revises: 20bc24429bfc
Create Date: 2023-06-09 17:58:31.519890

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd171ad09978'
down_revision = '20bc24429bfc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('payment', schema=None) as batch_op:
        batch_op.drop_constraint('payment_order_id_fkey', type_='foreignkey')
        batch_op.drop_column('order_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('payment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('order_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('payment_order_id_fkey', 'order', ['order_id'], ['id'])

    # ### end Alembic commands ###
