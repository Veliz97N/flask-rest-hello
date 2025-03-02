"""empty message

Revision ID: d91bab3d4e18
Revises: 
Create Date: 2021-11-22 23:42:37.540239

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd91bab3d4e18'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('planets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('rotation_period', sa.Float(), nullable=True),
    sa.Column('orbital_period', sa.Float(), nullable=True),
    sa.Column('diameter', sa.Float(), nullable=True),
    sa.Column('climate', sa.String(length=20), nullable=True),
    sa.Column('gravity', sa.String(length=20), nullable=True),
    sa.Column('terrain', sa.String(length=20), nullable=True),
    sa.Column('surface_water', sa.Float(), nullable=True),
    sa.Column('population', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('name')
    )
    op.create_table('starships',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('model', sa.String(length=50), nullable=True),
    sa.Column('length', sa.Integer(), nullable=True),
    sa.Column('starship_class', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=80), nullable=True),
    sa.Column('last_name', sa.String(length=80), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('email')
    )
    op.create_table('characters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('height', sa.Float(), nullable=True),
    sa.Column('mass', sa.Float(), nullable=True),
    sa.Column('hair_color', sa.String(length=50), nullable=True),
    sa.Column('skin_color', sa.String(length=50), nullable=True),
    sa.Column('eye_color', sa.String(length=50), nullable=True),
    sa.Column('birth_year', sa.String(length=50), nullable=True),
    sa.Column('gender', sa.String(length=15), nullable=True),
    sa.Column('starship', sa.Integer(), nullable=True),
    sa.Column('homeworld', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['homeworld'], ['planets.id'], ),
    sa.ForeignKeyConstraint(['starship'], ['starships.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_planet_fav',
    sa.Column('id_user', sa.Integer(), nullable=False),
    sa.Column('id_character', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_character'], ['planets.id'], ),
    sa.ForeignKeyConstraint(['id_user'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id_user', 'id_character')
    )
    op.create_table('user_starship_fav',
    sa.Column('id_user', sa.Integer(), nullable=False),
    sa.Column('id_starship', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_starship'], ['starships.id'], ),
    sa.ForeignKeyConstraint(['id_user'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id_user', 'id_starship')
    )
    op.create_table('user_character_fav',
    sa.Column('id_user', sa.Integer(), nullable=False),
    sa.Column('id_character', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_character'], ['characters.id'], ),
    sa.ForeignKeyConstraint(['id_user'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id_user', 'id_character')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_character_fav')
    op.drop_table('user_starship_fav')
    op.drop_table('user_planet_fav')
    op.drop_table('characters')
    op.drop_table('users')
    op.drop_table('starships')
    op.drop_table('planets')
    # ### end Alembic commands ###
