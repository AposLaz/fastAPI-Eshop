"""create table votes

Revision ID: 68de0c02fc84
Revises: 81cb4b852265
Create Date: 2021-12-09 10:34:43.377464

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.schema import Column


# revision identifiers, used by Alembic.
revision = '68de0c02fc84'
down_revision = '81cb4b852265'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('votes',
                    sa.Column('item_id', sa.Integer(), sa.ForeignKey('items.id', ondelete=('CASCADE')), primary_key=True),
                    sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete=('CASCADE')), primary_key=True)
                    )
    pass


def downgrade():
    pass
