"""banner_and_index_entrance

Revision ID: 0b54bbfc62f1
Revises: b5d8b14eee1b
Create Date: 2020-05-04 14:48:29.996478

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b54bbfc62f1'
down_revision = 'b5d8b14eee1b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Banner',
    sa.Column('isdelete', sa.Boolean(), nullable=True),
    sa.Column('createtime', sa.DateTime(), nullable=True),
    sa.Column('updatetime', sa.DateTime(), nullable=True),
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('position', sa.Integer(), nullable=True),
    sa.Column('img_url', sa.Text(), nullable=True),
    sa.Column('content_link', sa.Text(), nullable=True),
    sa.Column('item_order', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('IndexEntrance',
    sa.Column('isdelete', sa.Boolean(), nullable=True),
    sa.Column('createtime', sa.DateTime(), nullable=True),
    sa.Column('updatetime', sa.DateTime(), nullable=True),
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('img_url', sa.Text(), nullable=True),
    sa.Column('content_link', sa.Text(), nullable=True),
    sa.Column('item_order', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('IndexEntrance')
    op.drop_table('Banner')
    # ### end Alembic commands ###