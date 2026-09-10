CREATE TABLE transactions (id INTEGER PRIMARY KEY AUTOINCREMENT, reference TEXT NOT NULL UNIQUE, type TEXT NOT NULL, priority TEXT NOT NULL DEFAULT 'عادية', subject TEXT NOT NULL, entity TEXT NOT NULL, identity_number TEXT, department TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'قيد الإجراء', sla_days INTEGER NOT NULL DEFAULT 3, due_at TEXT NOT NULL, delay_reason TEXT, created_at TEXT NOT NULL, updated_at TEXT NOT NULL, created_by TEXT NOT NULL);
--> statement-breakpoint
CREATE TABLE transaction_events (id INTEGER PRIMARY KEY AUTOINCREMENT, transaction_id INTEGER NOT NULL REFERENCES transactions(id) ON DELETE CASCADE, action TEXT NOT NULL, details TEXT NOT NULL, department TEXT, actor TEXT NOT NULL, created_at TEXT NOT NULL);
--> statement-breakpoint
CREATE TABLE comments (id INTEGER PRIMARY KEY AUTOINCREMENT, transaction_id INTEGER NOT NULL REFERENCES transactions(id) ON DELETE CASCADE, body TEXT NOT NULL, author TEXT NOT NULL, created_at TEXT NOT NULL);
--> statement-breakpoint
CREATE TABLE attachments (id INTEGER PRIMARY KEY AUTOINCREMENT, transaction_id INTEGER NOT NULL REFERENCES transactions(id) ON DELETE CASCADE, object_key TEXT NOT NULL, filename TEXT NOT NULL, content_type TEXT NOT NULL, size_bytes INTEGER NOT NULL, uploaded_by TEXT NOT NULL, created_at TEXT NOT NULL);
--> statement-breakpoint
CREATE TABLE letter_templates (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, category TEXT NOT NULL, body TEXT NOT NULL, active INTEGER NOT NULL DEFAULT 1, created_at TEXT NOT NULL, updated_at TEXT NOT NULL);
--> statement-breakpoint
CREATE TABLE audit_logs (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT NOT NULL, user_email TEXT, action TEXT NOT NULL, resource_type TEXT NOT NULL, resource_id TEXT, details TEXT, ip_address TEXT, created_at TEXT NOT NULL);
--> statement-breakpoint
CREATE INDEX idx_transactions_status_department ON transactions(status, department);
--> statement-breakpoint
CREATE INDEX idx_transactions_type_created ON transactions(type, created_at);
--> statement-breakpoint
CREATE INDEX idx_transactions_priority ON transactions(priority);
--> statement-breakpoint
CREATE INDEX idx_events_transaction ON transaction_events(transaction_id, created_at);
--> statement-breakpoint
CREATE INDEX idx_audit_created ON audit_logs(created_at);
