WITH ranked_events AS (
    SELECT event_id, user_id, event_name, event_at, consent,
           ROW_NUMBER() OVER (PARTITION BY event_id ORDER BY received_at DESC) AS version
    FROM events
    WHERE julianday(event_at) <= julianday(:as_of)
      AND julianday(received_at) <= julianday(:as_of)
),
usable_events AS (
    SELECT event_id, user_id, event_name, event_at
    FROM ranked_events WHERE version = 1 AND consent = 1
),
signups AS (
    SELECT user_id, MIN(event_at) AS signup_at
    FROM usable_events WHERE event_name = 'signup'
    GROUP BY user_id
),
activation AS (
    SELECT s.user_id, MIN(e.event_at) AS activation_at
    FROM signups s JOIN usable_events e ON e.user_id = s.user_id
    WHERE e.event_name = 'core_action'
      AND julianday(e.event_at) - julianday(s.signup_at) >= 0
      AND julianday(e.event_at) - julianday(s.signup_at) < 8
    GROUP BY s.user_id
),
retention AS (
    SELECT s.user_id, MIN(e.event_at) AS retention_at
    FROM signups s JOIN activation a ON a.user_id = s.user_id
    JOIN usable_events e ON e.user_id = s.user_id
    WHERE e.event_name = 'core_action'
      AND julianday(e.event_at) - julianday(s.signup_at) >= 30
      AND julianday(e.event_at) - julianday(s.signup_at) < 60
    GROUP BY s.user_id
),
expansion AS (
    SELECT s.user_id, MIN(e.event_at) AS expansion_at
    FROM signups s JOIN activation a ON a.user_id = s.user_id
    JOIN usable_events e ON e.user_id = s.user_id
    WHERE e.event_name = 'upgrade'
      AND julianday(e.event_at) >= julianday(a.activation_at)
      AND julianday(e.event_at) - julianday(s.signup_at) < 90
    GROUP BY s.user_id
),
per_user AS (
    SELECT substr(s.signup_at, 1, 7) AS cohort_month,
           u.segment, u.market,
           CASE WHEN a.activation_at IS NOT NULL THEN 1 ELSE 0 END AS activated,
           CASE WHEN a.activation_at IS NOT NULL
                     AND julianday(:as_of) - julianday(s.signup_at) >= 60
                THEN 1 ELSE 0 END AS retention_eligible,
           CASE WHEN r.retention_at IS NOT NULL
                     AND julianday(:as_of) - julianday(s.signup_at) >= 60
                THEN 1 ELSE 0 END AS retained,
           CASE WHEN x.expansion_at IS NOT NULL THEN 1 ELSE 0 END AS expanded
    FROM signups s JOIN users u ON u.user_id = s.user_id
    LEFT JOIN activation a ON a.user_id = s.user_id
    LEFT JOIN retention r ON r.user_id = s.user_id
    LEFT JOIN expansion x ON x.user_id = s.user_id
)
SELECT cohort_month, segment, market,
       COUNT(*) AS acquired,
       SUM(activated) AS activated,
       SUM(retention_eligible) AS retention_eligible,
       SUM(retained) AS retained,
       SUM(expanded) AS expanded,
       ROUND(1.0 * SUM(activated) / COUNT(*), 4) AS acquisition_to_activation,
       CASE WHEN SUM(retention_eligible) > 0
            THEN ROUND(1.0 * SUM(retained) / SUM(retention_eligible), 4)
            ELSE NULL END AS eligible_retention_rate,
       CASE WHEN SUM(activated) > 0
            THEN ROUND(1.0 * SUM(expanded) / SUM(activated), 4)
            ELSE NULL END AS activation_to_expansion
FROM per_user
GROUP BY cohort_month, segment, market
ORDER BY cohort_month, segment, market;
