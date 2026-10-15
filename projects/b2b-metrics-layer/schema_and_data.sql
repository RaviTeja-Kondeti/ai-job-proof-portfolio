PRAGMA foreign_keys = ON;
CREATE TABLE accounts (
  account_id TEXT PRIMARY KEY,
  segment TEXT NOT NULL
);
CREATE TABLE product_events (
  event_id TEXT PRIMARY KEY,
  account_id TEXT NOT NULL REFERENCES accounts(account_id),
  event_type TEXT NOT NULL,
  event_day TEXT NOT NULL
);
CREATE TABLE opportunities (
  opportunity_id TEXT PRIMARY KEY,
  account_id TEXT NOT NULL REFERENCES accounts(account_id),
  stage TEXT NOT NULL CHECK (stage IN ('open','lost','won')),
  amount_usd INTEGER NOT NULL CHECK (amount_usd >= 0)
);
CREATE TABLE invoices (
  invoice_id TEXT PRIMARY KEY,
  account_id TEXT NOT NULL REFERENCES accounts(account_id),
  status TEXT NOT NULL CHECK (status IN ('paid','void')),
  amount_usd INTEGER NOT NULL CHECK (amount_usd >= 0)
);

INSERT INTO accounts VALUES ('a1','startup'),('a2','enterprise'),('a3','enterprise');
INSERT INTO product_events VALUES
 ('e1','a1','project_created','2026-09-01'),
 ('e2','a1','agent_run','2026-09-02'),
 ('e3','a2','project_created','2026-09-01'),
 ('e4','a2','agent_run','2026-09-03'),
 ('e5','a2','agent_run','2026-09-04');
INSERT INTO opportunities VALUES
 ('o1','a1','open',10000),
 ('o2','a1','won',5000),
 ('o3','a2','open',30000),
 ('o4','a2','open',10000),
 ('o5','a3','lost',20000);
INSERT INTO invoices VALUES
 ('i1','a1','paid',5000),
 ('i2','a1','paid',1000),
 ('i3','a2','paid',20000),
 ('i4','a2','void',2000);
