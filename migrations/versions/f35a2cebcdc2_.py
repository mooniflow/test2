"""empty message

Revision ID: f35a2cebcdc2
Revises: 6b19e64d1a03
Create Date: 2023-10-05 15:12:13.147700

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f35a2cebcdc2'
down_revision = '6b19e64d1a03'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('modify_date', sa.DateTime(), nullable=True))

    with op.batch_alter_table('posting', schema=None) as batch_op:
        batch_op.add_column(sa.Column('modify_date', sa.DateTime(), nullable=True))

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_user_username'), ['username'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_user_username'), type_='unique')

    with op.batch_alter_table('posting', schema=None) as batch_op:
        batch_op.drop_column('modify_date')

    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.drop_column('modify_date')

    # ### end Alembic commands ###