# Automated Cybersecurity Event Analytics & Suspicious Activity Detection System

## Abstract

This project develops an automated cybersecurity analytics system that
processes synthetic security events, calculates risk scores, detects
unusual activity, generates alerts, and presents analytical results
through a Tableau dashboard.

The system uses Python for data processing and analytics, PostgreSQL
for structured data storage, Isolation Forest for anomaly detection,
and Tableau for visualization.

## Table of Contents

1. Introduction
2. Literature Review
3. System Analysis
4. Methodology and System Design
5. Implementation
6. Testing and Validation
7. Results and Discussion
8. Conclusion and Future Scope
9. References
10. Appendices

## Chapter 1: Introduction

- Background and overview
- Problem statement
- Objectives
- Scope of the project
- Limitations

## Chapter 2: Literature Review

- Cybersecurity event analytics
- Rule-based detection
- Anomaly detection
- Isolation Forest
- Hybrid risk scoring
- Dashboard-based monitoring

## Chapter 3: System Analysis

- Problem definition
- Existing system
- Proposed system
- Feasibility study
- Functional requirements
- Non-functional requirements
- Hardware and software requirements

## Chapter 4: Methodology and System Design

- System architecture
- Synthetic data generation
- Data validation and ETL
- Database design
- Rule-based risk scoring
- Isolation Forest anomaly detection
- Hybrid risk score calculation
- Alert generation
- Tableau dashboard design

## Chapter 5: Implementation

- Technologies used
- Project folder structure
- Python implementation modules
- PostgreSQL integration
- Risk score storage
- Alert storage
- SQL views
- Tableau integration
- Python execution outputs

## Chapter 6: Testing and Validation

- Testing strategy
- Test cases
- Data consistency checks
- Database integrity checks
- Duplicate alert prevention
- Test results and limitations

## Chapter 7: Results and Discussion

- Risk classification results
- Hybrid risk score analysis
- Alert generation results
- Tableau dashboard analysis
- Interpretation of results

## Chapter 8: Conclusion and Future Scope

- Project summary
- Achievements
- Current limitations
- Future enhancements
- Conclusion

## Chapter 9: References

- Python documentation
- PostgreSQL documentation
- pandas documentation
- scikit-learn documentation
- Tableau documentation
- Relevant research papers

## Appendices

- Selected Python code
- SQL verification queries
- Python execution outputs
- Database screenshots
- Tableau dashboard screenshots
- Additional testing evidence

## Chapter 1: Introduction

- Background and overview
- Problem statement
- Objectives
- Scope of the project
- Limitations

## Chapter 1: Introduction

### 1.1 Background and Overview

Cybersecurity is an important aspect of modern information technology.
Organizations use computers, networks, applications, and databases to
store and process information. These systems generate security-related
events, including login attempts, authentication failures, successful
logins, and other activities.

Analyzing these events helps identify unusual behaviour and potential
security risks. However, manually examining a large number of events
can be time-consuming and may make it difficult to identify suspicious
patterns quickly.

The Automated Cybersecurity Event Analytics & Suspicious Activity
Detection System is designed to demonstrate how data analytics and
machine learning can support security event monitoring.

The system uses Python for data processing and analysis, PostgreSQL
for storing structured security information, rule-based scoring for
assessing risk, and Isolation Forest for identifying potentially
unusual events. A hybrid scoring approach combines rule-based and
anomaly-detection results. Tableau is used to visualize the analytical
results.

The project uses synthetic security event data. Therefore, its results
demonstrate the working of an analytics system rather than proving
the detection of real-world cyberattacks.

### 1.2 Problem Statement

Security systems can generate large volumes of event data. Examining
these events individually makes it difficult to summarize activity,
prioritize potentially suspicious events, and communicate findings
effectively.

A structured analytical approach is required to validate event data,
store it systematically, calculate risk scores, identify unusual
patterns, and generate alerts for further investigation.

This project addresses the problem by developing a prototype that
integrates data processing, database storage, risk scoring, anomaly
detection, alert generation, and dashboard-based visualization.

### 1.3 Objectives of the Project

The main objectives are:

1. To generate synthetic security event data for analysis.
2. To validate event data before performing analytics.
3. To store security events and analytical results in PostgreSQL.
4. To implement rule-based risk scoring.
5. To use the Isolation Forest algorithm to identify potentially
   anomalous events.
6. To calculate a hybrid risk score using rule-based and anomaly
   detection results.
7. To generate alerts for events that meet the configured risk
   threshold.
8. To create SQL views for summarizing security information.
9. To visualize risk distribution, risk scores, and event patterns
   through Tableau.
10. To evaluate the system using database checks, test cases, and
    observed execution results.

### 1.4 Scope of the Project

The project focuses on developing an analytical prototype for
cybersecurity event monitoring.

Its scope includes:

- Synthetic security event generation.
- Data validation and preprocessing.
- Structured storage using PostgreSQL.
- Python-based analytical processing.
- Rule-based risk scoring.
- Machine-learning-based anomaly detection.
- Hybrid risk score calculation.
- Alert generation and duplicate prevention.
- SQL views for analytical reporting.
- Tableau dashboards for visual exploration.
- Testing and validation of implemented components.

The project is intended for academic demonstration and experimentation.
It does not replace a production Security Information and Event
Management (SIEM) platform or a professional security operations team.

### 1.5 Limitations

The current implementation has several limitations:

1. The system uses synthetic data rather than live security logs.
2. The generated dataset may not represent the full complexity of
   real-world cyberattacks.
3. The Isolation Forest model identifies statistical anomalies, which
   are not necessarily malicious activities.
4. The dataset does not provide verified attack labels for calculating
   real-world detection accuracy.
5. Rule-based scoring depends on predefined thresholds and weights.
6. The current implementation does not provide continuous monitoring
   of a live network.
7. The Tableau dashboard uses exported CSV snapshots, so its displayed
   results may not automatically update when the database changes.
8. The system has not been validated in a production cybersecurity
   environment.

These limitations define the current boundaries of the prototype and
provide opportunities for future improvement.

## Chapter 2: Literature Review

- Cybersecurity event analytics
- Rule-based detection
- Anomaly detection
- Isolation Forest
- Hybrid risk scoring
- Dashboard-based monitoring

## Chapter 2: Literature Review

### 2.1 Introduction

A literature review examines the concepts, techniques, and technologies
relevant to a project. This chapter discusses cybersecurity event
analytics, rule-based detection, anomaly detection, the Isolation Forest
algorithm, hybrid risk scoring, and dashboard-based monitoring.

These concepts provide the foundation for developing an analytical
system that processes security events and highlights potentially
suspicious activities.

### 2.2 Cybersecurity Event Analytics

Cybersecurity event analytics involves collecting, processing, and
examining security-related records to understand system activity and
identify potentially suspicious patterns.

Examples of security events include failed login attempts, successful
authentication, access from different IP addresses, and device-related
activities.

Data analytics can help organize these records, calculate summary
statistics, identify patterns, and prioritize events for investigation.

In this project, Python and pandas are used to process security event
data, while PostgreSQL stores structured records and analytical results.
SQL views provide summarized information for dashboard visualization.

### 2.3 Rule-Based Detection

Rule-based detection uses predefined conditions to assign risk levels
or identify events that require further investigation.

For example, repeated failed login attempts may indicate a possible
authentication risk. A rule can assign additional risk points when
the number of failed attempts exceeds a specified threshold.

The main advantages of rule-based detection are simplicity,
interpretability, and ease of implementation. Analysts can understand
why a particular rule contributes to an event's risk score.

However, rule-based systems depend on predefined conditions. They may
not identify unusual patterns that do not match the configured rules.

In this project, rule-based scoring assigns risk points according to
configured conditions, including failed login activity. The resulting
score is capped at 100 and used to classify events into risk levels.

### 2.4 Anomaly Detection

Anomaly detection identifies observations that differ from patterns
considered normal within a dataset.

In cybersecurity analytics, unusual patterns may include unexpected
event frequencies, abnormal authentication behaviour, or activities
that differ from the general distribution of observed events.

An anomaly is not necessarily an attack. Legitimate users may also
produce unusual activity because of changes in their working
patterns, devices, or locations.

Anomaly detection can complement predefined rules by identifying
statistical patterns that are not explicitly represented by those
rules.

This project applies a machine-learning approach to selected security
event features to identify potentially anomalous observations.

### 2.5 Isolation Forest Algorithm

Isolation Forest is an unsupervised machine-learning algorithm used
for anomaly detection. It identifies observations that can be isolated
relatively easily through random partitioning of feature values.

The algorithm builds isolation trees using randomly selected features
and split values. Observations that require shorter average path
lengths to become isolated are generally considered more anomalous.

The main advantages of Isolation Forest include its ability to work
without labelled attack examples and its suitability for analysing
multidimensional data.

However, its output depends on the input features and model
configuration. Detected anomalies must not automatically be treated
as confirmed security incidents.

In this project, the model uses selected features such as failed
login activity, successful login activity, authentication failure
status, hour of day, and user event frequency.

The implementation uses the scikit-learn IsolationForest estimator
with a contamination parameter of 0.05 and a random state of 42.

The contamination parameter influences the expected proportion of
observations classified as anomalies; it does not establish that
exactly 5% of observations are malicious.

### 2.6 Hybrid Risk Scoring

A hybrid risk scoring approach combines outputs from multiple
analytical methods to produce a consolidated score.

Rule-based scoring provides interpretable risk indicators based on
predefined conditions. Anomaly detection provides a separate signal
based on unusual patterns in the data.

Combining these signals can provide a broader analytical view than
using either method independently.

In this project, the anomaly score is normalized to a 0–100 scale.
The hybrid score combines the rule-based score and normalized anomaly
score using the following weighted formula:

Hybrid Score = (0.60 × Rule Score) + (0.40 × Anomaly Score)

The rule-based component receives a weight of 60%, while the anomaly
component receives a weight of 40%.

The resulting score is used to assign a risk category. The configured
categories are Low, Medium, and High, based on the thresholds defined
in the risk-scoring implementation.

These weights are design choices for the prototype. They have not
been established as optimal through a labelled validation dataset.

### 2.7 Alert-Based Monitoring

Alert-based monitoring converts analytical results into records that
can be reviewed by an analyst.

An alert may contain an event identifier, alert type, severity,
status, and creation timestamp. Threshold-based alert generation
helps prioritize events that require attention.

In this project, alerts are generated when the hybrid risk score
meets the configured threshold of 40. Alerts are assigned Medium
severity for scores below 70 and High severity for scores of 70
or above.

The database uses a uniqueness constraint on the combination of
event identifier and alert type to help prevent duplicate alerts.

These alerts indicate events selected for review; they do not
confirm that a cyberattack has occurred.

### 2.8 Dashboard-Based Monitoring

Dashboards present analytical information through visualizations
that help users understand patterns and compare results.

Charts can summarize risk distributions, compare average risk scores,
and show changes in event activity over time.

Tableau is used in this project to present selected analytical results.
The dashboard includes security risk distribution, average hybrid
risk score by risk level, and security events by type over time.

The current Tableau Public workflow uses exported CSV snapshots
generated from database views. Consequently, the displayed data
represents the exported snapshot and does not automatically refresh
whenever PostgreSQL records change.

### 2.9 Research Gap and Project Motivation

Rule-based detection and anomaly detection address different aspects
of security event analysis. Rule-based methods provide transparent
conditions, while anomaly detection identifies statistically unusual
observations.

A small academic prototype can demonstrate how these approaches
can be combined with database storage, alert generation, and
dashboard visualization in a single analytical workflow.

The motivation for this project is to implement and evaluate such
an integrated workflow using synthetic security event data.

The project does not claim to replace production security platforms
or establish real-world detection accuracy. Instead, it demonstrates
the technical integration of data engineering, analytical scoring,
unsupervised learning, and visualization.

### 2.10 Chapter Summary

This chapter introduced the principal concepts supporting the
project. It discussed cybersecurity event analytics, rule-based
detection, anomaly detection, Isolation Forest, hybrid risk scoring,
alert-based monitoring, and dashboard visualization.

These concepts form the foundation for the system analysis and
implementation described in the following chapters.

## Chapter 3: System Analysis

- Problem definition
- Existing system
- Proposed system
- Feasibility study
- Functional requirements
- Non-functional requirements
- Hardware and software requirements

## Chapter 3: System Analysis

### 3.1 Introduction

System analysis identifies the problem to be solved, examines existing
approaches, and defines the requirements of the proposed system.

The Automated Cybersecurity Event Analytics & Suspicious Activity
Detection System integrates data processing, database management,
risk scoring, anomaly detection, alert generation, and visualization.

This chapter describes the existing approach, proposed solution,
feasibility, and system requirements.

### 3.2 Problem Definition

Security event records may contain information about authentication
attempts, user activity, timestamps, and other security-related events.

Examining these records individually can make it difficult to
summarize activity, identify unusual patterns, and prioritize events
for investigation.

The project addresses this problem by implementing an analytical
workflow that processes security event data, calculates risk scores,
identifies potential anomalies, and generates alerts based on
configured thresholds.

The system also presents selected results through a Tableau
dashboard to make the analysis easier to understand.

### 3.3 Existing System

In a basic security monitoring workflow, events may be examined
manually or evaluated using predefined rules.

Manual examination can become time-consuming as the number of
records increases. Rule-based approaches are easier to interpret,
but they may not identify unusual patterns that do not match
their predefined conditions.

Another challenge is that event processing, risk assessment,
alert management, and visualization may be handled separately.

The limitations discussed here describe the challenges addressed
by this project; they should not be interpreted as a claim that
all existing cybersecurity platforms have these limitations.

### 3.4 Proposed System

The proposed system integrates several components into one
analytical workflow.

The main components are:

1. Synthetic Security Event Generator
2. PostgreSQL Database
3. Python Data Processing and ETL
4. Rule-Based Risk Scoring
5. Isolation Forest Anomaly Detection
6. Hybrid Risk Score Calculation
7. Alert Generation and Storage
8. SQL Analytical Views
9. Tableau Dashboard

The generator creates synthetic security events. Python processes
and analyzes the data, while PostgreSQL stores the relevant records.

The risk engine calculates rule-based scores and combines them
with normalized anomaly scores. Events meeting the configured
alert threshold are selected for further review.

SQL views summarize the results for visualization. Tableau presents
the exported data through charts and dashboard components.

The current implementation is a prototype and does not continuously
monitor a live network.

### 3.5 System Workflow

The workflow is as follows:

1. Generate synthetic security event records.
2. Validate the generated data.
3. Load and process the required records.
4. Store security information in PostgreSQL.
5. Calculate rule-based risk scores.
6. Apply Isolation Forest to the selected analytical features.
7. Normalize the anomaly score and calculate the hybrid score.
8. Store the risk results in the database.
9. Generate alerts for events meeting the configured threshold.
10. Create analytical summaries using SQL views.
11. Export the required view results as CSV files.
12. Import the CSV snapshots into Tableau.
13. Analyze risk distributions and event patterns using the dashboard.

This workflow separates data preparation, analysis, storage,
alerting, and visualization into identifiable stages.

### 3.6 Feasibility Study

#### 3.6.1 Technical Feasibility

The project uses established technologies, including Python,
PostgreSQL, pandas, scikit-learn, and Tableau.

These technologies support data processing, relational data storage,
machine learning, and visualization.

The prototype can be implemented on a standard personal computer
without requiring dedicated enterprise security infrastructure.

#### 3.6.2 Economic Feasibility

The project can be developed primarily with free or open-source
software and synthetic data.

Python, PostgreSQL, pandas, and scikit-learn are available without
a software licence fee for ordinary use. Tableau Public provides
a free visualization option subject to its publishing and data
handling conditions.

Hardware, electricity, internet access, and development time
remain practical costs.

#### 3.6.3 Operational Feasibility

The workflow uses familiar development and analytical tools.
Python scripts automate processing tasks, PostgreSQL organizes
data, and Tableau presents analytical summaries.

The prototype can be used for academic demonstrations and
experimentation. It would require additional engineering,
monitoring, and security controls before production deployment.

#### 3.6.4 Schedule Feasibility

The project is divided into modules so that each component can
be implemented and tested separately.

The modular structure supports incremental development, debugging,
documentation, and integration.

### 3.7 Functional Requirements

Functional requirements describe what the system must do.

FR-01: Generate synthetic security event data.

FR-02: Validate relevant data fields before analysis.

FR-03: Store security event records in PostgreSQL.

FR-04: Calculate rule-based risk scores.

FR-05: Apply Isolation Forest to selected event features.

FR-06: Calculate a hybrid risk score using the configured weights.

FR-07: Classify events into Low, Medium, and High risk categories.

FR-08: Generate alerts for events meeting the configured threshold.

FR-09: Store risk results and alerts in the database.

FR-10: Prevent duplicate alert records for the same event and
alert type through database constraints and application logic.

FR-11: Provide SQL views for analytical summaries.

FR-12: Export analytical results for Tableau visualization.

FR-13: Display risk distribution, average risk scores, and event
patterns in the dashboard.

### 3.8 Non-Functional Requirements

Non-functional requirements describe the expected quality and
operational characteristics of the system.

#### Reliability

The system should validate input data and handle database
operations consistently. Database constraints should help
maintain data integrity.

#### Maintainability

The project should use separate modules for data generation,
ETL, risk scoring, anomaly detection, alert management, and
database operations.

#### Usability

The Tableau dashboard should present results through clearly
labelled charts and understandable risk categories.

#### Performance

The prototype should process its current synthetic dataset
without unnecessary computational overhead. Performance on
large production datasets has not yet been established.

#### Data Integrity

Records should maintain consistent relationships between
events, users, devices, and analytical results.

#### Reproducibility

Configured random seeds and documented parameters should make
the synthetic data generation and model configuration easier
to reproduce, subject to software versions and execution settings.

#### Security and Privacy

The prototype should avoid storing real credentials or exposing
database secrets in source control. Synthetic data should be
used for demonstrations unless appropriate safeguards are
implemented for real data.

### 3.9 Hardware Requirements

The prototype can run on a typical personal computer.

Recommended development environment:

- Processor: Modern dual-core processor or better.
- RAM: 8 GB or more recommended.
- Storage: Sufficient free space for the project, database,
  Python environment, and exported datasets.
- Operating System: Windows, Linux, or macOS.
- Internet connection: Required for installing dependencies
  and accessing online documentation.

These are practical recommendations, not benchmark-derived
minimum hardware specifications.

### 3.10 Software Requirements

The project uses the following software and libraries:

| Software or Library | Purpose |
|---|---|
| Python | Data processing and application logic |
| pandas | Data manipulation and analysis |
| NumPy | Numerical operations |
| scikit-learn | Isolation Forest anomaly detection |
| PostgreSQL | Relational database storage |
| SQLAlchemy / psycopg2 | Python database connectivity |
| Tableau Public | Dashboard visualization |
| Git | Version control |
| GitHub | Source code hosting |
| Visual Studio Code | Development environment |

Exact installed versions should be recorded from the development
environment before final submission.

### 3.11 Chapter Summary

This chapter defined the problem, explained the proposed system,
and examined its feasibility and requirements.

The proposed prototype integrates synthetic data generation,
database storage, risk scoring, anomaly detection, alert generation,
and visualization.

The next chapter describes the system architecture and the
methodology used to implement these components.

## Chapter 4: Methodology and System Design

- System architecture
- Synthetic data generation
- Data validation and ETL
- Database design
- Rule-based risk scoring
- Isolation Forest anomaly detection
- Hybrid risk score calculation
- Alert generation
- Tableau dashboard design

## Chapter 4: Methodology and System Design

### 4.1 Introduction

This chapter explains the methodology and architecture of the
Automated Cybersecurity Event Analytics & Suspicious Activity
Detection System.

The system follows a modular approach in which data generation,
validation, database storage, risk assessment, anomaly detection,
alert generation, and visualization are implemented as separate
but connected components.

The workflow demonstrates how data analytics and machine learning
can support the identification and prioritization of potentially
suspicious security events.

### 4.2 System Architecture

The architecture consists of the following layers:

1. Data Generation Layer
2. Data Processing and Validation Layer
3. Database Layer
4. Analytics and Risk Assessment Layer
5. Alert Management Layer
6. Visualization Layer

#### 4.2.1 Data Generation Layer

The data generation module creates synthetic security event records
for analysis and testing.

The generated dataset contains 1,000 security events, along with
supporting user and device information.

Synthetic data makes it possible to experiment with analytical
techniques without relying on real users' security records.

#### 4.2.2 Data Processing and Validation Layer

The processing layer prepares event data for analysis.

Python and pandas are used to work with structured records.
Validation checks help identify inconsistencies and ensure that
the data meets the requirements of subsequent processing stages.

#### 4.2.3 Database Layer

PostgreSQL stores the structured security information and analytical
results.

The database contains tables for users, devices, IP addresses,
security events, login history, risk events, and alerts.

Relational storage allows the system to connect event information
with associated entities and analytical results.

#### 4.2.4 Analytics and Risk Assessment Layer

This layer calculates rule-based risk scores and applies Isolation
Forest to selected event features.

The two analytical signals are combined into a hybrid score.
The resulting score is used to classify events into risk categories.

#### 4.2.5 Alert Management Layer

The alert management module selects events whose hybrid scores
meet the configured threshold.

The resulting alerts are stored in PostgreSQL for review.
A database uniqueness constraint helps prevent duplicate alerts
for the same event and alert type.

#### 4.2.6 Visualization Layer

SQL views provide summarized analytical information.

The required results are exported as CSV snapshots and imported
into Tableau Public. The dashboard displays risk distribution,
average hybrid risk scores, and security event patterns over time.

The current visualization workflow uses exported snapshots rather
than a continuously refreshed live database connection.

### 4.3 Overall Data Flow

The system follows this sequence:

Synthetic Data Generation
        |
        v
Data Validation and Processing
        |
        v
PostgreSQL Database
        |
        v
Rule-Based Risk Scoring
        |
        v
Isolation Forest Anomaly Detection
        |
        v
Hybrid Risk Score Calculation
        |
        v
Risk Results Stored in PostgreSQL
        |
        v
Alert Generation and Storage
        |
        v
SQL Analytical Views
        |
        v
CSV Export
        |
        v
Tableau Dashboard

The workflow separates data preparation from analytical processing
and presentation. This makes individual components easier to test,
maintain, and improve.

### 4.4 Synthetic Data Generation

Synthetic data is generated to simulate security-related activity.

The dataset includes information such as event timestamps, user
identifiers, device identifiers, IP addresses, event types, and
authentication-related fields.

The generator also creates supporting user and device records so
that events can be associated with relevant entities.

Synthetic data has several advantages for this project:

- It avoids the need to collect real user security logs.
- It supports repeatable experiments.
- It allows controlled test scenarios.
- It simplifies debugging and validation.
- It can be shared for academic demonstration with fewer privacy
  concerns than real security data.

However, synthetic data may not capture the diversity and complexity
of real-world security activity.

### 4.5 Data Validation and ETL

ETL stands for Extract, Transform, and Load.

The ETL process prepares source data for reliable analytical use.

#### Extract

The extraction stage reads the generated security event data and
accesses the required information for processing.

#### Transform

The transformation stage checks data quality, prepares fields,
and validates relationships between relevant records.

Typical checks include:

- Missing or invalid values.
- Duplicate records where uniqueness is expected.
- Incorrect data types.
- Invalid timestamps.
- Inconsistent user and device relationships.
- Invalid authentication-related combinations.

#### Load

The loading stage places the prepared records into the appropriate
database tables or makes them available to the downstream
analytical pipeline.

Validation helps reduce the possibility that inconsistent input
will distort subsequent analysis.

### 4.6 Database Design

PostgreSQL is used as the relational database management system.

The main tables are:

| Table | Purpose |
|---|---|
| users | Stores user-related information |
| devices | Stores device-related information |
| ip_addresses | Stores IP address records |
| security_events | Stores security event information |
| login_history | Stores login-related records |
| risk_events | Stores analytical risk results |
| alerts | Stores generated alert records |

The `security_events` table acts as the central source of event
information. Supporting tables provide associated user, device,
network, login, risk, and alert information.

The `risk_events` table stores the rule score, anomaly score,
hybrid score, and risk classification associated with an event.

The `alerts` table stores alerts generated by the alert management
component.

Database constraints help preserve integrity and prevent certain
types of duplicate records.

### 4.7 Rule-Based Risk Scoring

Rule-based scoring assigns points to events according to predefined
conditions.

The implementation considers failed login activity and includes
additional points when the failed login count reaches the configured
threshold.

The scoring function can also consider whether an IP address or
device is new. However, the current event-level calculation uses
`False` for both the new-IP and new-device flags. These two factors
therefore do not contribute to the current calculated scores.

The scoring rules are:

| Condition | Risk Points |
|---|---:|
| At least one failed login | +10 |
| Five or more failed logins | +40 |
| New IP address | +20 |
| New device | +20 |
| Maximum score | 100 |

The total is capped at 100.

The resulting score is classified using these thresholds:

| Score | Risk Level |
|---|---|
| Below 40 | Low |
| 40 to below 70 | Medium |
| 70 to 100 | High |

The event-level calculation uses a rolling five-minute failed-login
count per user.

These thresholds are configuration choices for the prototype.
They should not be interpreted as universally applicable measures
of cybersecurity risk.

### 4.8 Isolation Forest Anomaly Detection

Isolation Forest is an unsupervised machine-learning algorithm
used to identify observations that differ from the general
patterns in a dataset.

The implementation uses the following features:

- Failed login activity.
- Successful login activity.
- Authentication failure status.
- Hour of day.
- User event frequency.

The model is configured with:

- Contamination: 0.05
- Random state: 42

The contamination parameter influences the proportion of
observations the algorithm expects to classify as anomalous.

The model's output indicates statistical unusualness rather than
confirmed malicious behaviour. A legitimate event may be anomalous,
and a malicious event may not be detected.

The dataset does not contain verified attack labels for calculating
real-world detection accuracy.

### 4.9 Hybrid Risk Score Calculation

The hybrid scoring component combines the rule-based score with
the normalized anomaly score.

The formula is:

Hybrid Score = (0.60 × Rule Score) + (0.40 × Anomaly Score)

Here:

- Rule Score represents the rule-based risk score.
- Anomaly Score represents the anomaly score normalized to a
  scale of 0 to 100.
- 0.60 is the rule-score weight.
- 0.40 is the anomaly-score weight.

The rule-based component contributes 60% of the hybrid score,
while the anomaly component contributes 40%.

The formula combines interpretable rule conditions with an
additional signal derived from the statistical characteristics
of the event data.

The weights are selected for the prototype and have not been
optimized against a labelled validation dataset.

### 4.10 Alert Generation

The alert management module uses the hybrid risk score to determine
which events should generate alerts.

The configured alert threshold is 40.

Events meeting or exceeding this threshold are eligible for alert
generation.

Severity is assigned as follows:

| Hybrid Score | Alert Severity |
|---|---|
| 40 to below 70 | Medium |
| 70 or above | High |

Alerts are stored in PostgreSQL.

A unique database index on the combination of event identifier
and alert type helps prevent duplicate alert records.

The alert mechanism prioritizes events for review; it does not
confirm that an attack has occurred.

### 4.11 SQL Analytical Views

SQL views provide structured summaries for reporting and
visualization.

The project includes the following views:

- `vw_risk_overview`
- `vw_security_event_analysis`
- `vw_alert_monitoring`

The risk overview view summarizes risk classifications and scores.

The security event analysis view provides event-level information
for further analysis.

The alert monitoring view provides information about generated
alerts and their relevant attributes.

These views reduce the need to repeat complex query logic when
preparing data for dashboard visualization.

### 4.12 Tableau Dashboard Design

Tableau Public is used to present the analytical results.

The dashboard contains three principal visualizations:

1. Security Risk Distribution
2. Average Hybrid Risk Score by Risk Level
3. Security Events by Type Over Time

The risk distribution chart shows how many events belong to each
risk category.

The average score chart compares the mean hybrid score for
different risk levels.

The event timeline displays security event activity across time
and distinguishes event types.

The dashboard provides a visual summary of the analysis and
supports exploration of the synthetic dataset.

Because the current workflow uses CSV snapshots, the dashboard
must be refreshed by exporting and importing updated data when
the underlying database results change.

### 4.13 Chapter Summary

This chapter described the system architecture and the methodology
used by the prototype.

The system combines synthetic data generation, validation,
PostgreSQL storage, rule-based risk scoring, Isolation Forest
anomaly detection, hybrid scoring, alert management, SQL views,
and Tableau visualization.

The next chapter describes the software tools and implementation
modules used to construct the system.