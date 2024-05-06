"""Updated field name

Revision ID: 58b86fed7986
Revises: 01e600282266
Create Date: 2024-04-26 14:54:29.129008

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '58b86fed7986'
down_revision = '01e600282266'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('userPassword', sa.String(length=255), nullable=True))
        batch_op.drop_column('hashedPassword')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('hashedPassword', sa.VARCHAR(length=255), nullable=True))
        batch_op.drop_column('userPassword')

    # ### end Alembic commands ###
