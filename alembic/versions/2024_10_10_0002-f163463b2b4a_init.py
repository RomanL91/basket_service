"""init

Revision ID: f163463b2b4a
Revises: 
Create Date: 2024-10-10 00:02:02.377155

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f163463b2b4a"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "baskets",
        sa.Column("uuid_id", sa.String(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("completed", sa.Boolean(), nullable=True),
        sa.Column("basket_items", sa.JSON(), nullable=True),
        sa.Column("gift_items", sa.JSON(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("created_at"),
        sa.UniqueConstraint("uuid_id"),
    )
    op.create_table(
        "orders",
        sa.Column("user_full_name", sa.String(), nullable=False),
        sa.Column("total_amount", sa.DECIMAL(precision=10, scale=2), nullable=False),
        sa.Column("account_number", sa.Integer(), nullable=False),
        sa.Column(
            "payment_type",
            sa.Enum("ONLINE", "OFFLINE", name="paymenttype"),
            nullable=False,
        ),
        sa.Column("uuid_id", sa.String(), nullable=False),
        sa.Column(
            "order_status",
            sa.Enum(
                "NEW",
                "INWORK",
                "COMPLITED",
                "CANCELED",
                name="orderstatustype",
            ),
            nullable=False,
        ),
        sa.Column("comment", sa.Text(), nullable=True),
        sa.Column("phone_number", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("shipping_city", sa.String(), nullable=False),
        sa.Column("delivery_address", sa.String(), nullable=True),
        sa.Column(
            "delivery_type",
            sa.Enum("DELIVERY", "PICKUP", name="deliverytype"),
            nullable=False,
        ),
        sa.Column("manager_executive", sa.String(), nullable=True),
        sa.Column("manager_executive_id", sa.String(), nullable=True),
        sa.Column("manager_mailbox", sa.String(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["uuid_id"],
            ["baskets.uuid_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("account_number"),
        sa.UniqueConstraint("uuid_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("orders")
    op.drop_table("baskets")
    # ### end Alembic commands ###
