"""empty message

Revision ID: a66c68168f2e
Revises: 2d51e8d43ae8
Create Date: 2018-03-24 18:19:38.737539

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a66c68168f2e'
down_revision = '2d51e8d43ae8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reading', sa.Column('uv', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('reading', 'uv')
    # ### end Alembic commands ###
