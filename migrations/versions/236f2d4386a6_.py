"""empty message

Revision ID: 236f2d4386a6
Revises: 
Create Date: 2021-12-04 11:50:33.177985

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '236f2d4386a6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('User',
    sa.Column('photo', sa.String(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.Unicode(length=128), nullable=False),
    sa.Column('first_name', sa.Unicode(length=128), nullable=False),
    sa.Column('last_name', sa.Unicode(length=128), nullable=False),
    sa.Column('password', sa.Unicode(length=128), nullable=True),
    sa.Column('birthdate', sa.DateTime(), nullable=True),
    sa.Column('reports', sa.Integer(), nullable=True),
    sa.Column('points', sa.Integer(), nullable=True),
    sa.Column('is_blocked', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('BadWord',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('word', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Blacklist',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('id_user', sa.Integer(), nullable=True),
    sa.Column('id_blacklisted', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_blacklisted'], ['User.id'], ),
    sa.ForeignKeyConstraint(['id_user'], ['User.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Blacklist')
    op.drop_table('BadWord')
    op.drop_table('User')
    # ### end Alembic commands ###
