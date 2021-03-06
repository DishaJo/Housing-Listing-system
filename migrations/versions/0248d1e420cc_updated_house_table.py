"""Updated House Table

Revision ID: 0248d1e420cc
Revises: 10905a1c6025
Create Date: 2022-06-20 13:19:56.994152

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0248d1e420cc'
down_revision = '10905a1c6025'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('house', sa.Column('user_id', sa.Integer(), nullable=False))
    op.drop_constraint('house_user_fkey', 'house', type_='foreignkey')
    op.create_foreign_key(None, 'house', 'user', ['user_id'], ['user_id'])
    op.drop_column('house', 'user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('house', sa.Column('user', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'house', type_='foreignkey')
    op.create_foreign_key('house_user_fkey', 'house', 'user', ['user'], ['user_id'])
    op.drop_column('house', 'user_id')
    # ### end Alembic commands ###
