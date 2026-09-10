ALTER TABLE transactions ADD COLUMN archived_at TEXT;

CREATE INDEX idx_transactions_archive_type
ON transactions(archived_at, type);

PRAGMA optimize;
