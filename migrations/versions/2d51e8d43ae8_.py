"""empty message

Revision ID: 2d51e8d43ae8
Revises: a124b8c5f582
Create Date: 2018-03-24 14:26:47.847154

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d51e8d43ae8'
down_revision = 'a124b8c5f582'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reading', sa.Column('pi_id', sa.Integer(), nullable=True))
    op.add_column('reading', sa.Column('pi_serial', sa.String(), nullable=True))
    op.add_column('result', sa.Column('pi_id', sa.Integer(), nullable=True))
    op.add_column('result', sa.Column('pi_serial', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('result', 'pi_serial')
    op.drop_column('result', 'pi_id')
    op.drop_column('reading', 'pi_serial')
    op.drop_column('reading', 'pi_id')
    # ### end Alembic commands ###
