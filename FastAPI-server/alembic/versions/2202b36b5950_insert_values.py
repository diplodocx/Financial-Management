"""insert_values

Revision ID: 2202b36b5950
Revises: 943616cbe805
Create Date: 2023-04-30 23:43:51.935075

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy.orm import Session

from src.manager.models import payment, user, category

revision = '2202b36b5950'
down_revision = '943616cbe805'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.bulk_insert(user, [
        {'hashed_password': '$2b$12$Jb2G7adspyHp/1jk8.ZW6u4L2G50XPA13XUCyaThp03eTRMhMxRSO', 'email': 'test@test.com',
         'is_active': True, 'is_superuser': False, 'is_verified': False}
    ])
    op.bulk_insert(category, [
        {'category_name': 'housing', 'payment_type': 'spending'},
        {'category_name': 'food', 'payment_type': 'spending'},
        {'category_name': 'transportation', 'payment_type': 'spending'},
        {'category_name': 'healthcare', 'payment_type': 'spending'},
        {'category_name': 'entertainment', 'payment_type': 'spending'},
        {'category_name': 'clothing', 'payment_type': 'spending'},
        {'category_name': 'communications', 'payment_type': 'spending'},
        {'category_name': 'education', 'payment_type': 'spending'},
        {'category_name': 'household expenses', 'payment_type': 'spending'},
        {'category_name': 'pets', 'payment_type': 'spending'},
        {'category_name': 'debts', 'payment_type': 'spending'},
        {'category_name': 'other', 'payment_type': 'spending'},
        {'category_name': 'salary', 'payment_type': 'receiving'},
        {'category_name': 'gifts', 'payment_type': 'receiving'},
        {'category_name': 'rent', 'payment_type': 'receiving'},
        {'category_name': 'wins', 'payment_type': 'receiving'},
        {'category_name': 'debts', 'payment_type': 'receiving'},
        {'category_name': 'savings', 'payment_type': 'receiving'},
        {'category_name': 'state payments', 'payment_type': 'receiving'},
        {'category_name': 'other', 'payment_type': 'receiving'}
    ])
    op.bulk_insert(payment, [
        {'amount': 500.0, 'method': 'RUB', 'owner': 1, 'category': 13},
        {'amount': 300.0, 'method': 'RUB', 'owner': 1, 'category': 15},
        {'amount': 200.0, 'method': 'RUB', 'owner': 1, 'category': 2},
        {'amount': 600.0, 'method': 'RUB', 'owner': 1, 'category': 1},
    ])


def downgrade() -> None:
    bind = op.get_bind()
    session = Session(bind=bind)
    stmt = payment.delete()
    session.execute(stmt)
    stmt = user.delete()
    session.execute(stmt)
    stmt = category.delete()
    session.execute(stmt)
    session.commit()
