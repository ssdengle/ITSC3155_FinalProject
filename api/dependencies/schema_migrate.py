"""
Apply additive schema updates for MySQL DBs that existed before new columns were added.
SQLAlchemy create_all() does not ALTER existing tables.
"""

from sqlalchemy import text
from sqlalchemy.exc import OperationalError


def _ignorable_mysql_alter(err: OperationalError) -> bool:
    """Duplicate column (1060) or duplicate index/key name (1061)."""
    orig = getattr(err, "orig", None)
    if orig is not None and getattr(orig, "args", None):
        code = orig.args[0]
        if code in (1060, 1061):
            return True
    msg = str(err).lower()
    if "duplicate column" in msg or "duplicate key" in msg or "already exists" in msg:
        return True
    return False


def apply_checklist_migrations(engine) -> None:
    alters = [
        "ALTER TABLE sandwiches ADD COLUMN tags VARCHAR(500) NULL",
        "ALTER TABLE orders ADD COLUMN tracking_number VARCHAR(32) NULL",
        "ALTER TABLE orders ADD COLUMN order_type VARCHAR(20) NOT NULL DEFAULT 'takeout'",
        "ALTER TABLE orders ADD COLUMN order_status VARCHAR(30) NOT NULL DEFAULT 'pending'",
        "ALTER TABLE orders ADD COLUMN total_price DECIMAL(10, 2) NULL",
        "ALTER TABLE reviews MODIFY COLUMN customer_id INT NULL",
        "ALTER TABLE reviews ADD COLUMN guest_name VARCHAR(100) NULL",
    ]
    indexes = [
        "CREATE UNIQUE INDEX idx_orders_tracking ON orders (tracking_number)",
    ]
    with engine.begin() as conn:
        for sql in alters:
            try:
                conn.execute(text(sql))
            except OperationalError as e:
                if not _ignorable_mysql_alter(e):
                    raise
        for sql in indexes:
            try:
                conn.execute(text(sql))
            except OperationalError as e:
                if not _ignorable_mysql_alter(e):
                    raise
