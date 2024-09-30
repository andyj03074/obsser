"""empty message

Revision ID: 88bd2ac9080a
Revises: 6e759a66af0c
Create Date: 2024-09-24 21:25:32.714445

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '88bd2ac9080a'
down_revision = '6e759a66af0c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('place_info',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('tag', sa.String(length=20), nullable=False),
    sa.Column('type', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product_detail_info',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('likes_count', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('product_detail_info')
    op.drop_table('place_info')
    # ### end Alembic commands ###
