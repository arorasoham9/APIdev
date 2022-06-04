"""create posts table

Revision ID: ed70b24f14a3
Revises: 
Create Date: 2022-06-04 04:09:59.784705

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed70b24f14a3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column(('id'), sa.Integer(), nullable= False, primary_key = True)
    pass


def downgrade() -> None:
    pass
