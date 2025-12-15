CREATE TABLE IF NOT EXISTS menna.events
(
    event_date Date DEFAULT toDate(timestamp),
    timestamp DateTime DEFAULT now(),
    event String,
    user_id String,
    provider_id String,
    city String,
    category String,
    metadata Map(String, String)
)
ENGINE = MergeTree()
PARTITION BY event_date
ORDER BY (event, timestamp);

-- Example queries:
-- Conversion by city/category:
-- SELECT city, category,
--        countIf(event='lead_created') AS leads,
--        countIf(event='provider_contact_clicked') AS contact_clicks,
--        contact_clicks / NULLIF(leads,0) AS ctr
-- FROM menna.events
-- WHERE event IN ('lead_created','provider_contact_clicked')
-- GROUP BY city, category
-- ORDER BY ctr DESC;

-- Leads per day:
-- SELECT event_date, count(*) FROM menna.events
-- WHERE event='lead_created'
-- GROUP BY event_date ORDER BY event_date;
