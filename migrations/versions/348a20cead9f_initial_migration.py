"""Initial migration

Revision ID: 348a20cead9f
Revises: 
Create Date: 2024-11-23 15:21:08.294163

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '348a20cead9f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('last_name', sqlmodel.sql.sqltypes.AutoString(length=50), nullable=False),
    sa.Column('first_name', sqlmodel.sql.sqltypes.AutoString(length=50), nullable=False),
    sa.Column('middle_name', sqlmodel.sql.sqltypes.AutoString(length=50), nullable=False),
    sa.Column('address', sqlmodel.sql.sqltypes.AutoString(length=200), nullable=False),
    sa.Column('phone', sqlmodel.sql.sqltypes.AutoString(length=20), nullable=False),
    sa.Column('email', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
    sa.Column('is_regular', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
    sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('unit', sa.Enum('KG', 'PIECES', 'LITERS', 'METERS', 'PACK', name='unitenum'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sales',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=False),
    sa.Column('sale_date', sa.DateTime(), nullable=False),
    sa.Column('delivery_date', sa.DateTime(), nullable=False),
    sa.Column('quantity', sa.Numeric(precision=10, scale=3), nullable=False),
    sa.ForeignKeyConstraint(['client_id'], ['clients.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sales')
    op.drop_table('products')
    op.drop_table('clients')
    # ### end Alembic commands ###
