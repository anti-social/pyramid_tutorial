"""products: add status field

Revision ID: 17de29a15aa0
Revises: 4fb207f28a50
Create Date: 2020-05-13 13:01:16.017722

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17de29a15aa0'
down_revision = '4fb207f28a50'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('status', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('products', 'status')
    # ### end Alembic commands ###
