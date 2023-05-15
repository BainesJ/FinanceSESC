"""empty message

Revision ID: 2583bf356bca
Revises: 9b4d98a18671
Create Date: 2021-09-01 12:34:56.7890123

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2583bf356bca'
down_revision = '9b4d98a18671'
branch_labels = None
depends_on = None


def upgrade():
    # Set the enumeration values
    type_enum_values = ('COURSE_FEE', 'LIBRARY_FEE')
    status_enum_values = ('OUTSTANDING', 'PAID', 'CANCELLED')

    # Replace the empty enumeration definition with the specified values
    with op.batch_alter_table('invoice', schema=None) as batch_op:
        batch_op.alter_column(
            'type',
            existing_type=sa.Enum(),
            nullable=True,
            server_default=None,
            type_=sa.Enum(*type_enum_values, name='type')
        )
        batch_op.alter_column(
            'status',
            existing_type=sa.Enum(),
            nullable=False,
            server_default='OUTSTANDING',
            type_=sa.Enum(*status_enum_values, name='status')
        )


def downgrade():
    # Set the enumeration values
    type_enum_values = ('COURSE_FEE', 'LIBRARY_FEE')
    status_enum_values = ('OUTSTANDING', 'PAID', 'CANCELLED')

    # Replace the specified enumeration values with an empty enumeration definition
    with op.batch_alter_table('invoice', schema=None) as batch_op:
        batch_op.alter_column(
            'type',
            existing_type=sa.Enum(*type_enum_values, name='type'),
            nullable=True,
            server_default=None,
            type_=sa.Enum(),
        )
        batch_op.alter_column(
            'status',
            existing_type=sa.Enum(*status_enum_values, name='status'),
            nullable=False,
            server_default='OUTSTANDING',
            type_=sa.Enum(),
        )
