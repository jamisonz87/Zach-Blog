"""empty message

Revision ID: 7498ed38eb98
Revises: 32598b3865c5
Create Date: 2020-06-12 14:34:22.824082

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7498ed38eb98'
down_revision = '32598b3865c5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('mark_url', sa.String(length=50), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('post_mark_url', sa.VARCHAR(length=50), nullable=True))
    op.drop_column('post', 'mark_url')
    # ### end Alembic commands ###
