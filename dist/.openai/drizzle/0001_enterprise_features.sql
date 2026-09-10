CREATE TABLE app_users (id TEXT PRIMARY KEY, email TEXT, name TEXT, role TEXT NOT NULL DEFAULT 'registrar', department TEXT, job_title TEXT, active INTEGER NOT NULL DEFAULT 1, created_at TEXT NOT NULL, updated_at TEXT NOT NULL);
--> statement-breakpoint
CREATE TABLE departments (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, parent_id INTEGER REFERENCES departments(id), sla_days INTEGER NOT NULL DEFAULT 5, active INTEGER NOT NULL DEFAULT 1);
--> statement-breakpoint
CREATE TABLE entities (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, entity_type TEXT NOT NULL, contact_name TEXT, phone TEXT, email TEXT, active INTEGER NOT NULL DEFAULT 1, created_at TEXT NOT NULL, updated_at TEXT NOT NULL);
--> statement-breakpoint
CREATE TABLE holidays (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, holiday_date TEXT NOT NULL UNIQUE);
--> statement-breakpoint
CREATE TABLE app_settings (setting_key TEXT PRIMARY KEY, setting_value TEXT NOT NULL, updated_at TEXT NOT NULL);
--> statement-breakpoint
CREATE TABLE notifications (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT NOT NULL, transaction_id INTEGER REFERENCES transactions(id), title TEXT NOT NULL, body TEXT NOT NULL, read_at TEXT, created_at TEXT NOT NULL);
--> statement-breakpoint
ALTER TABLE transactions ADD COLUMN external_reference TEXT;
--> statement-breakpoint
ALTER TABLE transactions ADD COLUMN external_date TEXT;
--> statement-breakpoint
ALTER TABLE transactions ADD COLUMN channel TEXT;
--> statement-breakpoint
ALTER TABLE transactions ADD COLUMN confidentiality TEXT NOT NULL DEFAULT 'عادي';
--> statement-breakpoint
ALTER TABLE transactions ADD COLUMN keywords TEXT;
--> statement-breakpoint
ALTER TABLE transactions ADD COLUMN linked_transaction_id INTEGER REFERENCES transactions(id);
--> statement-breakpoint
ALTER TABLE transactions ADD COLUMN assignee_id TEXT;
--> statement-breakpoint
ALTER TABLE transactions ADD COLUMN cancelled_at TEXT;
--> statement-breakpoint
CREATE INDEX idx_transactions_department_status ON transactions(department,status);
--> statement-breakpoint
CREATE INDEX idx_notifications_user_read ON notifications(user_id,read_at);
