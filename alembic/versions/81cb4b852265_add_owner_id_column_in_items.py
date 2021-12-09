"""add owner_id column in items

Revision ID: 81cb4b852265
Revises: 404123a33bb6
Create Date: 2021-12-09 10:16:39.806536

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.schema import ForeignKey


# revision identifiers, used by Alembic.
revision = '81cb4b852265'
down_revision = '404123a33bb6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('items',
                  sa.Column('owner_id', sa.Integer(), sa.ForeignKey('users.id', ondelete=('CASCADE')), nullable=False)
                  )
    pass


def downgrade():
    pass
