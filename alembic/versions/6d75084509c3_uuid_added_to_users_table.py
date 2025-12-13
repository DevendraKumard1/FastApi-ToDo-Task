"""Add uuid column to users table (not null, unique)

Revision ID: 6d75084509c3
Revises: 6a3f6cc10419
Create Date: 2025-12-04
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "6d75084509c3"
down_revision: Union[str, Sequence[str], None] = "6a3f6cc10419"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1️⃣ Add uuid column as NULLABLE
    op.add_column(
        "users",
        sa.Column("uuid", sa.CHAR(36), nullable=True)
    )

    # 2️⃣ Populate UNIQUE UUIDs for all existing rows
    # UUID() generates a unique value per row in MySQL
    op.execute("""
        UPDATE users
        SET uuid = UUID()
        WHERE uuid IS NULL
    """)

    # 3️⃣ Enforce NOT NULL
    # MySQL requires MODIFY instead of ALTER COLUMN
    op.execute("""
        ALTER TABLE users
        MODIFY uuid CHAR(36) NOT NULL
    """)

    # 4️⃣ Add UNIQUE constraint
    op.create_unique_constraint(
        "uq_users_uuid",
        "users",
        ["uuid"]
    )


def downgrade() -> None:
    op.drop_constraint("uq_users_uuid", "users", type_="unique")
    op.drop_column("users", "uuid")
