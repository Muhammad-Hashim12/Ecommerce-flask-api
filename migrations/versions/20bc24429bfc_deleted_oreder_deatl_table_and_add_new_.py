"""deleted oreder deatl table and add new column to payment table

Revision ID: 20bc24429bfc
Revises: de266002f184
Create Date: 2023-06-09 11:24:18.447307

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20bc24429bfc'
down_revision = 'de266002f184'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order__detail')
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.add_column(sa.Column('total_prize', sa.Integer(), nullable=True))
        batch_op.drop_column('total_cost')

    with op.batch_alter_table('payment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('total_cost', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('address', sa.String(length=255), nullable=False))
        batch_op.add_column(sa.Column('order_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'order', ['order_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('payment', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('order_id')
        batch_op.drop_column('address')
        batch_op.drop_column('total_cost')

    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.add_column(sa.Column('total_cost', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_column('total_prize')

    op.create_table('order__detail',
    sa.Column('od_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('add', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('order_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('customer_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], name='order__detail_customer_id_fkey'),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], name='order__detail_order_id_fkey'),
    sa.PrimaryKeyConstraint('od_id', name='order__detail_pkey')
    )
    # ### end Alembic commands ###