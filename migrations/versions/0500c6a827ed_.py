"""empty message

Revision ID: 0500c6a827ed
Revises: 189b1da162e8
Create Date: 2024-09-28 12:33:28.041871

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0500c6a827ed'
down_revision = '189b1da162e8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('productinfo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('myproduct',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('productinfo_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['productinfo_id'], ['productinfo.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'productinfo_id')
    )
    op.drop_table('product_detail_info')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product_detail_info',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=150), nullable=False),
    sa.Column('price', sa.INTEGER(), nullable=False),
    sa.Column('description', sa.VARCHAR(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('myproduct')
    op.drop_table('productinfo')
    # ### end Alembic commands ###
