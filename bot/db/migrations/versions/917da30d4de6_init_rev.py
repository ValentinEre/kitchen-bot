"""Init rev

Revision ID: 917da30d4de6
Revises: 
Create Date: 2023-08-24 21:36:25.502147

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '917da30d4de6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('Intermediate_Ingredients_ingredient_id_fk', 'Intermediate', type_='foreignkey')
    op.drop_constraint('Intermediate_Units_unit_id_fk', 'Intermediate', type_='foreignkey')
    op.drop_constraint('Intermediate_Receipts__fk', 'Intermediate', type_='foreignkey')
    op.alter_column('Receipts', 'preparation',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Receipts', 'preparation',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.create_foreign_key('Intermediate_Receipts__fk', 'Intermediate', 'Receipts', ['recept_id'], ['recept_id'])
    op.create_foreign_key('Intermediate_Units_unit_id_fk', 'Intermediate', 'Units', ['unit_id'], ['unit_id'])
    op.create_foreign_key('Intermediate_Ingredients_ingredient_id_fk', 'Intermediate', 'Ingredients', ['ingredient_id'], ['ingredient_id'])
    # ### end Alembic commands ###
