"""phone not required

Revision ID: 462581f4c702
Revises: 6a4cc7d02007
Create Date: 2022-07-10 16:42:11.782497

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '462581f4c702'
down_revision = '6a4cc7d02007'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('admins', 'phone',
               existing_type=sa.VARCHAR(length=14),
               nullable=True)
    op.alter_column('analysts', 'phone',
               existing_type=sa.VARCHAR(length=14),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('analysts', 'phone',
               existing_type=sa.VARCHAR(length=14),
               nullable=False)
    op.alter_column('admins', 'phone',
               existing_type=sa.VARCHAR(length=14),
               nullable=False)
    # ### end Alembic commands ###