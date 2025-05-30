"""added showtime id to seatbooking

Revision ID: 94789c83561b
Revises: ffc18c7f12dd
Create Date: 2025-04-15 07:59:31.616611

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94789c83561b'
down_revision = 'ffc18c7f12dd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('seat_booking', schema=None) as batch_op:
        batch_op.add_column(sa.Column('showtime_id', sa.Integer(), nullable=False, default=1))  # Use a default value
        batch_op.create_foreign_key('fk_showtime_id', 'showtime', ['showtime_id'], ['id'])

    # ### end Alembic commands ###



def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('seat_booking', schema=None) as batch_op:
        batch_op.drop_constraint('fk_showtime_id', type_='foreignkey')
        batch_op.drop_column('showtime_id')

    # ### end Alembic commands ###
