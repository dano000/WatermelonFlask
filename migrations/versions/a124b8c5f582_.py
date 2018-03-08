"""empty message

Revision ID: a124b8c5f582
Revises: 033922c382f8
Create Date: 2018-03-08 22:43:39.536464

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a124b8c5f582'
down_revision = '033922c382f8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('result',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('s3_key', sa.String(), nullable=True),
    sa.Column('etag', sa.String(), nullable=True),
    sa.Column('ripe', sa.Boolean(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reading',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('reading', postgresql.ARRAY(sa.Integer()), nullable=True),
    sa.Column('laser', sa.Boolean(), nullable=True),
    sa.Column('led', sa.Boolean(), nullable=True),
    sa.Column('result_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['result_id'], ['result.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('results')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('results',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('s3_key', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('etag', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('ripe', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('timestamp', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='results_pkey')
    )
    op.drop_table('reading')
    op.drop_table('result')
    # ### end Alembic commands ###
