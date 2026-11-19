CREATE OR REPLACE VIEW vw_risk_overview AS
SELECT
    risk_level,
    COUNT(*) AS event_count,
    ROUND(AVG(hybrid_score)::numeric, 2) AS average_hybrid_score,
    ROUND(MAX(hybrid_score)::numeric, 2) AS maximum_hybrid_score
FROM risk_events
GROUP BY risk_level;

CREATE OR REPLACE VIEW vw_security_event_analysis AS
SELECT
    se.event_id,
    se.event_timestamp,
    se.event_type,
    se.user_id,
    se.device_id,
    se.location,
    se.auth_status,
    re.rule_score,
    re.anomaly_score,
    re.hybrid_score,
    re.risk_level
FROM security_events AS se
LEFT JOIN risk_events AS re
    ON re.event_id = se.event_id;

CREATE OR REPLACE VIEW vw_alert_monitoring AS
SELECT
    alert_id,
    event_id,
    alert_type,
    alert_message,
    severity,
    alert_status,
    created_at,
    resolved_at
FROM alerts;