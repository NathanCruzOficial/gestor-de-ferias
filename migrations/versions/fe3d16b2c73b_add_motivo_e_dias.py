"""add motivo e dias

Revision ID: fe3d16b2c73b
Revises: 8850b3eaad06
Create Date: 2025-01-20 19:34:14.448493

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe3d16b2c73b'
down_revision = '8850b3eaad06'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Ferias', schema=None) as batch_op:
        batch_op.add_column(sa.Column('motivo', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('dias', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Ferias', schema=None) as batch_op:
        batch_op.drop_column('dias')
        batch_op.drop_column('motivo')

    # ### end Alembic commands ###
