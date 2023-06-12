"""added new table Payment and Payment_details

Revision ID: bcea3d8bf454
Revises: fd171ad09978
Create Date: 2023-06-12 11:05:35.247691

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'bcea3d8bf454'
down_revision = 'fd171ad09978'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('payment__detail',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(length=255), nullable=False),
    sa.Column('payment_date', sa.DateTime(), nullable=True),
    sa.Column('is_payed', sa.Boolean(), nullable=True),
    sa.Column('customer_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('payment', schema=None) as batch_op:
        batch_op.drop_column('payment_date')
        batch_op.drop_column('is_payed')
        batch_op.drop_column('address')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('payment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('address', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('is_payed', sa.BOOLEAN(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('payment_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))

    op.drop_table('payment__detail')
    # ### end Alembic commands ###