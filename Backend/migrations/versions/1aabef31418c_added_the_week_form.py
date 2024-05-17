"""added the week form

Revision ID: 1aabef31418c
Revises: aac714af405a
Create Date: 2024-05-17 16:26:42.264341

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1aabef31418c'
down_revision = 'aac714af405a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('time_range',
    sa.Column('ID', sa.Integer(), nullable=False),
    sa.Column('groupID', sa.Integer(), nullable=False),
    sa.Column('day', sa.String(length=10), nullable=True),
    sa.Column('start_time', sa.Time(), nullable=True),
    sa.Column('stop_time', sa.Time(), nullable=True),
    sa.ForeignKeyConstraint(['groupID'], ['users.userID'], ),
    sa.PrimaryKeyConstraint('ID')
    )
    with op.batch_alter_table('time_range', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_time_range_groupID'), ['groupID'], unique=False)

    op.create_table('time_slot',
    sa.Column('ID', sa.Integer(), nullable=False),
    sa.Column('groupID', sa.Integer(), nullable=False),
    sa.Column('day', sa.String(length=10), nullable=False),
    sa.Column('start_time', sa.Time(), nullable=False),
    sa.Column('end_time', sa.Time(), nullable=False),
    sa.ForeignKeyConstraint(['groupID'], ['groups.groupID'], ),
    sa.PrimaryKeyConstraint('ID')
    )
    with op.batch_alter_table('time_slot', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_time_slot_groupID'), ['groupID'], unique=False)

    with op.batch_alter_table('groups', schema=None) as batch_op:
        batch_op.drop_column('fridayEndTime')
        batch_op.drop_column('tuesdayEndTime')
        batch_op.drop_column('webnesdayStartTime')
        batch_op.drop_column('fridayStartTime')
        batch_op.drop_column('saterdayStartTime')
        batch_op.drop_column('thursdayStartTime')
        batch_op.drop_column('tuesdayStartTime')
        batch_op.drop_column('sundayEndTime')
        batch_op.drop_column('webnesdayEndTime')
        batch_op.drop_column('mondayStartTime')
        batch_op.drop_column('saterdayEndTime')
        batch_op.drop_column('thursdayEndTime')
        batch_op.drop_column('mondayEndTime')
        batch_op.drop_column('sundayStartTime')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('groups', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sundayStartTime', sa.VARCHAR(length=16), nullable=False))
        batch_op.add_column(sa.Column('mondayEndTime', sa.VARCHAR(length=16), nullable=False))
        batch_op.add_column(sa.Column('thursdayEndTime', sa.VARCHAR(length=16), nullable=False))
        batch_op.add_column(sa.Column('saterdayEndTime', sa.VARCHAR(length=16), nullable=False))
        batch_op.add_column(sa.Column('mondayStartTime', sa.VARCHAR(length=16), nullable=False))
        batch_op.add_column(sa.Column('webnesdayEndTime', sa.VARCHAR(length=16), nullable=False))
        batch_op.add_column(sa.Column('sundayEndTime', sa.VARCHAR(length=16), nullable=False))
        batch_op.add_column(sa.Column('tuesdayStartTime', sa.VARCHAR(length=16), nullable=False))
        batch_op.add_column(sa.Column('thursdayStartTime', sa.VARCHAR(length=16), nullable=False))
        batch_op.add_column(sa.Column('saterdayStartTime', sa.VARCHAR(length=16), nullable=False))
        batch_op.add_column(sa.Column('fridayStartTime', sa.VARCHAR(length=16), nullable=False))
        batch_op.add_column(sa.Column('webnesdayStartTime', sa.VARCHAR(length=16), nullable=False))
        batch_op.add_column(sa.Column('tuesdayEndTime', sa.VARCHAR(length=16), nullable=False))
        batch_op.add_column(sa.Column('fridayEndTime', sa.VARCHAR(length=16), nullable=False))

    with op.batch_alter_table('time_slot', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_time_slot_groupID'))

    op.drop_table('time_slot')
    with op.batch_alter_table('time_range', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_time_range_groupID'))

    op.drop_table('time_range')
    # ### end Alembic commands ###