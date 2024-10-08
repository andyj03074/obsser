"""empty message

Revision ID: 8cb9ce964b50
Revises: 
Create Date: 2024-10-02 00:47:38.627122

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8cb9ce964b50'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('inquiry',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=150), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('notice',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('placeinfo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('tag', sa.String(length=20), nullable=False),
    sa.Column('type', sa.String(length=20), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('image', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('productinfo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('image', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('travelplan',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('date', sa.Integer(), nullable=False),
    sa.Column('image_url', sa.String(length=150), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=150), nullable=False),
    sa.Column('password', sa.String(length=200), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('myinquiry',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('inquiryinfo_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['inquiryinfo_id'], ['inquiry.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'inquiryinfo_id')
    )
    op.create_table('myplace',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('placeinfo_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['placeinfo_id'], ['placeinfo.id'], ondelete='cascade'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('user_id', 'placeinfo_id')
    )
    op.create_table('myproduct',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('productinfo_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['productinfo_id'], ['productinfo.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'productinfo_id')
    )
    op.create_table('mytravel',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('travelplan_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['travelplan_id'], ['travelplan.id'], ondelete='cascade'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('user_id', 'travelplan_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('mytravel')
    op.drop_table('myproduct')
    op.drop_table('myplace')
    op.drop_table('myinquiry')
    op.drop_table('user')
    op.drop_table('travelplan')
    op.drop_table('productinfo')
    op.drop_table('placeinfo')
    op.drop_table('notice')
    op.drop_table('inquiry')
    # ### end Alembic commands ###
