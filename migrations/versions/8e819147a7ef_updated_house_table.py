"""Updated House Table

Revision ID: 8e819147a7ef
Revises: 3163378c5057
Create Date: 2022-06-16 18:10:07.785965

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e819147a7ef'
down_revision = '3163378c5057'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('house', sa.Column('bhk', sa.Integer(), nullable=False))
    op.add_column('house', sa.Column('deposit', sa.String(length=20), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('house', 'deposit')
    op.drop_column('house', 'bhk')
    # ### end Alembic commands ###
