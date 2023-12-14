"""empty message

Revision ID: 38f0cf72293d
Revises: 3a98c4394eae
Create Date: 2023-09-22 14:11:41.526173

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '38f0cf72293d'
down_revision = '3a98c4394eae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('question_voter',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], name=op.f('fk_question_voter_question_id_question'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_question_voter_user_id_user'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'question_id', name=op.f('pk_question_voter'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('question_voter')
    # ### end Alembic commands ###
