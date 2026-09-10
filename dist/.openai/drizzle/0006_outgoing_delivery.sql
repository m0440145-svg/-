ALTER TABLE transactions ADD COLUMN delivery_receipt TEXT;
ALTER TABLE transactions ADD COLUMN approved_at TEXT;
PRAGMA optimize;
