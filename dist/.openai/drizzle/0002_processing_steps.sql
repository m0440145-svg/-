CREATE TABLE processing_steps (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  transaction_id INTEGER NOT NULL REFERENCES transactions(id) ON DELETE CASCADE,
  step_order INTEGER NOT NULL,
  action_text TEXT NOT NULL,
  result_text TEXT,
  status TEXT NOT NULL DEFAULT 'مكتملة',
  duration_minutes INTEGER,
  performed_by_id TEXT NOT NULL,
  performed_by_name TEXT NOT NULL,
  performed_at TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE INDEX idx_processing_steps_transaction_order
ON processing_steps(transaction_id, step_order);

PRAGMA optimize;
