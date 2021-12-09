"""create items table

Revision ID: 978772f35faa
Revises: 
Create Date: 2021-12-09 09:07:40.190353

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.sqltypes import String


# revision identifiers, used by Alembic.
revision = '978772f35faa'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('items', 
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('type', sa.String(), nullable=False),
                    sa.Column('description', sa.String(), nullable=False), 
                    sa.Column('tags', sa.ARRAY(String), nullable=False),
                    sa.Column('price', sa.Float(), nullable=False), 
                    sa.Column('available', sa.Boolean(), nullable=False),
                    sa.Column('inventory', sa.Integer(), nullable=False))
    pass


def downgrade():
    op.drop_table("items")
    pass
