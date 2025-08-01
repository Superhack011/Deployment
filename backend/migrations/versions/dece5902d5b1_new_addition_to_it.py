"""New Addition to it.

Revision ID: dece5902d5b1
Revises: 321c9ff8d7d5
Create Date: 2025-06-27 21:20:06.750136

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dece5902d5b1'
down_revision = '321c9ff8d7d5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('report', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=False))
        batch_op.alter_column('validity',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.Boolean(),
               existing_nullable=True)
        batch_op.create_foreign_key('fk_report_user_id', 'user', ['user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('report', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.alter_column('validity',
               existing_type=sa.Boolean(),
               type_=sa.VARCHAR(length=255),
               existing_nullable=True)
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###
