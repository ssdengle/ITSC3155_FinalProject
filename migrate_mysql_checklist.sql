-- Run manually against existing DBs that were created before checklist columns were added.
-- New installs: SQLAlchemy create_all() will create tables with these columns.

ALTER TABLE sandwiches ADD COLUMN tags VARCHAR(500) NULL;

ALTER TABLE orders ADD COLUMN tracking_number VARCHAR(32) NULL;
ALTER TABLE orders ADD UNIQUE INDEX idx_orders_tracking (tracking_number);
ALTER TABLE orders ADD COLUMN order_type VARCHAR(20) NOT NULL DEFAULT 'takeout';
ALTER TABLE orders ADD COLUMN order_status VARCHAR(30) NOT NULL DEFAULT 'pending';
ALTER TABLE orders ADD COLUMN total_price DECIMAL(10, 2) NULL;

ALTER TABLE reviews MODIFY COLUMN customer_id INT NULL;
ALTER TABLE reviews ADD COLUMN guest_name VARCHAR(100) NULL;
