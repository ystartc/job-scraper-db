"""Added autoincrement Id for Job model

Revision ID: eda2b2e8e21d
Revises: d8d50abff380
Create Date: 2023-08-04 09:45:08.556056

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eda2b2e8e21d'
down_revision = 'd8d50abff380'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('jobs', sa.Column('job_id', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('jobs', 'job_id')
    # ### end Alembic commands ###
