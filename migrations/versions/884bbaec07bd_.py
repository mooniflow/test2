"""empty message

Revision ID: 884bbaec07bd
Revises: fbaa51eb20e3
Create Date: 2023-10-06 13:54:07.027623

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '884bbaec07bd'
down_revision = 'fbaa51eb20e3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post_voter',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('pid', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['pid'], ['posting.id'], name=op.f('fk_post_voter_pid_posting'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['uid'], ['user.id'], name=op.f('fk_post_voter_uid_user'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('uid', 'pid', name=op.f('pk_post_voter'))
    )
    op.create_table('comment_voter',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('comment_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['comment_id'], ['comment.id'], name=op.f('fk_comment_voter_comment_id_comment'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_comment_voter_user_id_user'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'comment_id', name=op.f('pk_comment_voter'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment_voter')
    op.drop_table('post_voter')
    # ### end Alembic commands ###