# Cybersecurity Event Analytics and Suspicious Activity Detection

An end-to-end Python and PostgreSQL prototype for generating synthetic cybersecurity events, calculating risk scores, detecting unusual activity, creating security alerts, and presenting the results in Tableau.

## Current Project Status

The core prototype is implemented and has been run against a synthetic dataset of 1,000 events.

Implemented:

- Synthetic cybersecurity event generation
- Data extraction, transformation, validation, and PostgreSQL loading
- Rule-based risk scoring
- Isolation Forest anomaly detection
- Hybrid risk scoring
- Risk and alert storage in PostgreSQL
- Duplicate prevention for risk and alert records
- SQL tables, indexes, and database relationships
- Tableau dashboard documentation and CSV-based data sources
- Project report and recorded results documentation

Current limitations:

- Uses synthetic data rather than real security logs
- Has no verified attack labels for measuring detection accuracy
- Runs as a batch workflow, not continuous monitoring
- Tableau currently uses refreshed CSV snapshots rather than a direct live database connection
- New-IP and new-device indicators are supported by the scoring function but are not active in the current event-level calculation
- The recorded execution produced no High-risk events

## Recorded Results

For the current 1,000-event dataset:

| Risk level | Events | Average hybrid score |
|---|---:|---:|
| Low | 985 | 13.31 |
| Medium | 15 | 43.66 |
| High | 0 | Not applicable |

The run stored 1,000 risk records and generated 15 open Medium-severity alerts. No duplicate event/alert-type combinations were observed.

These results demonstrate the prototype workflow. They do not establish real-world detection accuracy.

## Architecture

```text
Synthetic Data Generator
          |
          v
CSV Dataset --> ETL Pipeline --> PostgreSQL
                                      |
                      Rule-Based Scoring
                                      |
                      Isolation Forest Anomaly Detection
                                      |
                      Hybrid Risk Scoring
                                      |
              Risk Records + Alert Records
                                      |
                         Tableau CSV Snapshots
```

## Detection Design

### Rule-based scoring

- Failed login: 10 points
- Five or more failed logins in the user's preceding five-minute window: additional 40 points
- New IP address: 20 points, when enabled
- New device: 20 points, when enabled
- Maximum score: 100

### Hybrid scoring

```text
Hybrid score = (60% * rule score) + (40% * normalized anomaly score)
```

| Hybrid score | Risk level | Alert severity |
|---|---|---|
| Below 40 | Low | None |
| 40 to below 70 | Medium | Medium |
| 70 to 100 | High | High |

Isolation Forest uses failed-login, successful-login, authentication-failure, hour-of-day, and user event-frequency features with a contamination of 5% and random state 42. Its output represents statistical unusualness, not confirmed malicious activity.

## Technology Stack

- Python
- Pandas and NumPy
- Scikit-learn
- PostgreSQL
- SQLAlchemy and psycopg2
- python-dotenv
- Matplotlib, Seaborn, and Plotly
- Tableau Public
- Git and GitHub

## Project Structure

```text
data/                    Generated and raw CSV datasets
database/sql/            PostgreSQL schema and SQL assets
docs/                    Results summary and dashboard screenshots
reports/                 Markdown and DOCX project reports
src/
  data_generator/        Synthetic event generation
  etl/                   Extraction, transformation, and validation
  database/              PostgreSQL connection
  risk_engine/           Rule, hybrid, and database risk logic
  anomaly_detection/     Isolation Forest implementation
  alerts/                Alert generation and storage
  analytics/             End-to-end analytics workflow
tableau/                 Tableau dashboard documentation
```

## Setup

### 1. Create and activate a virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 3. Configure PostgreSQL

Create a PostgreSQL database named `cybersecurity_db`, then apply the schema:

```powershell
psql -d cybersecurity_db -f database/sql/schema.sql
```

Create a `.env` file in the repository root:

```text
DB_USER=your_postgres_user
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=cybersecurity_db
```

Do not commit `.env` or database credentials.

## Running the Prototype

From the repository root, run the stages in sequence:

```powershell
python src/data_generator/generate_data.py
python src/etl/etl_pipeline.py
python src/analytics/analysis.py
```

The generator writes 1,000 events to `data/raw/security_events_raw.csv`. The ETL pipeline validates and loads the events and associated reference records. The analytics workflow calculates and stores risk scores and creates eligible alerts.

## Tableau Dashboard

The dashboard presents:

1. Security risk distribution
2. Average hybrid risk score by risk level
3. Security events by type over time

Dashboard documentation is available in [tableau/README.md](tableau/README.md). A screenshot is available in [docs/screenshots/tableau_dashboard.png](docs/screenshots/tableau_dashboard.png).

Tableau currently reads exported CSV snapshots. Refreshing the data requires rerunning the analytical workflow and updating the imported CSV files.

## Database Tables

- `users`
- `devices`
- `ip_addresses`
- `security_events`
- `login_history`
- `risk_events`
- `alerts`

The schema includes foreign keys and indexes for event, timestamp, severity, status, and risk-level queries. Unique indexes/constraints help prevent duplicate risk and alert entries.

## Documentation

- [Project report](reports/Project_Report.md)
- [Recorded project results](docs/PROJECT_RESULTS.md)
- [Tableau dashboard guide](tableau/README.md)

## Future Work

- Validate with labelled security datasets and calculate precision, recall, F1-score, and false-positive rates
- Activate and validate new-IP and new-device risk indicators
- Generate controlled High-risk and High-severity test scenarios
- Add real-time event ingestion and automated database refresh
- Connect Tableau directly to PostgreSQL
- Add analyst acknowledgment, investigation status, resolution notes, and audit history
- Extend filtering and drill-down views for users, devices, locations, event types, and time ranges
- Harden concurrent alert processing and deployment security
