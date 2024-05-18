"""Set message type to optional

Revision ID: c6a5aa218054
Revises: 226f861e2c82
Create Date: 2024-05-13 14:18:46.335678

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c6a5aa218054'
down_revision = '226f861e2c82'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('groups', schema=None) as batch_op:
        batch_op.alter_column('messages',
               existing_type=sa.VARCHAR(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('groups', schema=None) as batch_op:
        batch_op.alter_column('messages',
               existing_type=sa.VARCHAR(),
               nullable=False)

    # ### end Alembic commands ###
