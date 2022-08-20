"""Enum fix_1

Revision ID: 4ec5e4b033cd
Revises: 9f37f26dacff
Create Date: 2022-08-20 16:15:35.673601

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ec5e4b033cd'
down_revision = '9f37f26dacff'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('analysis', 'type')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('analysis', sa.Column('type', sa.VARCHAR(length=30), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
