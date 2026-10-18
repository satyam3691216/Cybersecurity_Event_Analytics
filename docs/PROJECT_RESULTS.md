# Project Results Summary

## 1. Project Overview

The Automated Cybersecurity Event Analytics & Suspicious
Activity Detection System analyzes synthetic security events
using rule-based risk scoring and Isolation Forest anomaly
detection.

The system stores security events, risk scores, and alerts
in PostgreSQL and visualizes analytical results using Tableau.

## 2. Dataset Summary

- Total synthetic security events: 1,000
- Data source: Programmatically generated synthetic data
- Storage: PostgreSQL
- Analytics: Python, Pandas, and Scikit-learn

## 3. Risk Classification Results

| Risk Level | Events | Average Hybrid Score | Maximum Score |
|------------|-------:|---------------------:|--------------:|
| Low        | 985    | 13.31                | 39.84         |
| Medium     | 15     | 43.66                | 66.55         |
| High       | 0      | Not applicable       | Not applicable|

## 4. Alert Results

- Total alerts: 15
- Medium-severity alerts: 15
- Open alerts: 15
- Duplicate event/type combinations: 0

## 5. Dashboard

The Tableau dashboard contains three visualizations:

1. Security Risk Distribution
2. Average Hybrid Risk Score by Risk Level
3. Security Events by Type Over Time

## 6. Limitations

- The dataset is synthetic, not collected from a live
  production environment.
- Ground-truth labels are unavailable, so detection accuracy
  has not been established.
- The current results contain no high-risk events.
- Tableau data exported from PostgreSQL as CSV files must
  be refreshed manually.

## 7. Future Improvements

- Evaluate the system against labeled security datasets.
- Add automated data refresh.
- Improve detection of new devices and unfamiliar IP addresses.
- Add high-risk alert scenarios and additional dashboard filters.
- Evaluate precision, recall, F1-score, and false-positive rate
  when reliable ground-truth labels are available.