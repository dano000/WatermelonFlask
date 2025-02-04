"""empty message

Revision ID: 033922c382f8
Revises: 
Create Date: 2018-03-05 17:30:10.458516

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '033922c382f8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('results',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('s3_key', sa.String(), nullable=True),
    sa.Column('etag', sa.String(), nullable=True),
    sa.Column('ripe', sa.Boolean(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('results')
    # ### end Alembic commands ###
