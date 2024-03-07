"""empty message

Revision ID: e612b812669c
Revises: 9d5b825d7279
Create Date: 2024-03-07 13:24:32.370289

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e612b812669c'
down_revision = '9d5b825d7279'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('game',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('title', sa.String(length=150), nullable=True),
    sa.Column('version', sa.String(length=150), nullable=True),
    sa.Column('publisher', sa.String(length=150), nullable=True),
    sa.Column('region', sa.String(length=75), nullable=True),
    sa.Column('completed', sa.Boolean(), nullable=True),
    sa.Column('status', sa.String(length=250), nullable=True),
    sa.Column('value', sa.DECIMAL(precision=7, scale=2), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('email', sa.String(length=150), nullable=False),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('g_auth_verify', sa.Boolean(), nullable=True),
    sa.Column('admin', sa.Boolean(), nullable=True),
    sa.Column('token', sa.String(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('token')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('game')
    # ### end Alembic commands ###