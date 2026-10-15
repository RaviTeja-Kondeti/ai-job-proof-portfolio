-- Preaggregate each one-to-many source at account grain before joining.
WITH usage AS (
  SELECT account_id,
         COUNT(*) AS event_count,
         SUM(CASE WHEN event_type = 'agent_run' THEN 1 ELSE 0 END) AS agent_runs
  FROM product_events
  GROUP BY account_id
),
pipeline AS (
  SELECT account_id,
         SUM(CASE WHEN stage = 'open' THEN amount_usd ELSE 0 END) AS open_pipeline_usd
  FROM opportunities
  GROUP BY account_id
),
revenue AS (
  SELECT account_id,
         SUM(CASE WHEN status = 'paid' THEN amount_usd ELSE 0 END) AS paid_revenue_usd
  FROM invoices
  GROUP BY account_id
)
SELECT a.account_id, a.segment,
       COALESCE(u.event_count, 0) AS event_count,
       COALESCE(u.agent_runs, 0) AS agent_runs,
       COALESCE(p.open_pipeline_usd, 0) AS open_pipeline_usd,
       COALESCE(r.paid_revenue_usd, 0) AS paid_revenue_usd
FROM accounts a
LEFT JOIN usage u USING (account_id)
LEFT JOIN pipeline p USING (account_id)
LEFT JOIN revenue r USING (account_id)
ORDER BY a.account_id;
