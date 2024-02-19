"""typo on available col

Revision ID: f40b4c8b87c8
Revises: 26c5608cabbf
Create Date: 2024-01-21 01:19:52.830090

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f40b4c8b87c8'
down_revision = '26c5608cabbf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tutor', schema=None) as batch_op:
        batch_op.add_column(sa.Column('available', sa.Boolean(), nullable=True))
        batch_op.drop_column('avaialable')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tutor', schema=None) as batch_op:
        batch_op.add_column(sa.Column('avaialable', sa.BOOLEAN(), autoincrement=False, nullable=True))
        batch_op.drop_column('available')

    # ### end Alembic commands ###