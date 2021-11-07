"""profile model changes

Revision ID: edd4b835cf17
Revises: e7af4e0df7db
Create Date: 2021-11-07 20:30:52.697812

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'edd4b835cf17'
down_revision = 'e7af4e0df7db'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password_hash', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('pass_secure', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'pass_secure')
    op.drop_column('users', 'password_hash')
    # ### end Alembic commands ###
