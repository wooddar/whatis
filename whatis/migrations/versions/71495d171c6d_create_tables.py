"""create tables

Revision ID: 71495d171c6d
Revises: 
Create Date: 2019-09-21 15:51:23.360753

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "71495d171c6d"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "whatis",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("terminology", sa.String(), nullable=False),
        sa.Column("definition", sa.String(), nullable=False),
        sa.Column("notes", sa.String(), nullable=True),
        sa.Column("links", sa.String(), nullable=True),
        sa.Column("submitted_at", sa.DateTime(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("added_by", sa.String(), nullable=False),
        sa.Column("point_of_contact", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("whatis")
    # ### end Alembic commands ###
