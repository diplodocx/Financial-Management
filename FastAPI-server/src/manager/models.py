from datetime import datetime
from sqlalchemy.orm import relationship
import sqlalchemy as db

metadata = db.MetaData()

user = db.Table(
    "user",
    metadata,
    db.Column("id", db.Integer, autoincrement=True, primary_key=True),
    db.Column("hashed_password", db.String(length=1024), nullable=False),
    db.Column("email", db.String(200), unique=True, nullable=False),
    db.Column("is_active", db.Boolean, default=True, nullable=False),
    db.Column("is_superuser", db.Boolean, default=False, nullable=False),
    db.Column("is_verified", db.Boolean, default=False, nullable=False),
    db.Column("wallet", db.Float, default=0.0)
)

category = db.Table(
    "category",
    metadata,
    db.Column("category_id", db.Integer, autoincrement=True, primary_key=True),
    db.Column("category_name", db.String(200), nullable=False),
    db.Column("payment_type", db.String(10), nullable=False)
)

payment = db.Table(
    "payment",
    metadata,
    db.Column("payment_id", db.Integer, autoincrement=True, primary_key=True),
    db.Column("payment_time", db.TIMESTAMP, default=datetime.now()),
    db.Column("amount", db.Float, nullable=False),
    db.Column("method", db.String(10), nullable=False),
    db.Column("comment", db.Text, default="-"),
    db.Column("owner", db.Integer, db.ForeignKey("user.id", ondelete='CASCADE', onupdate='CASCADE'), nullable=False),
    db.Column("category", db.Integer, db.ForeignKey("category.category_id", ondelete='CASCADE', onupdate='CASCADE'),
              nullable=False)
)
