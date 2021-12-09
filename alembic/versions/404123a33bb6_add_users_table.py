"""Add users table

Revision ID: 404123a33bb6
Revises: 978772f35faa
Create Date: 2021-12-09 09:25:33.728445

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '404123a33bb6'
down_revision = '978772f35faa'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users", 
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('username', sa.String(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('telephone', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'),
                    sa.UniqueConstraint('username')
                    )
    pass


def downgrade():
    op.drop_table("users")
    pass
