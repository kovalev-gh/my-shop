from typing import Sequence, Union

from alembic import op

# revision identifiers
revision = "469a3814d4aa"
down_revision = "1eb9cc3b5412"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("ALTER TYPE orderstatus ADD VALUE 'waiting_payment'")


def downgrade() -> None:
    # PostgreSQL не поддерживает удаление ENUM значения напрямую
    # поэтому downgrade делается либо пустым, либо через пересоздание типа
    pass