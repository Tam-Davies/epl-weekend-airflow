# Premier League Weekend Data Pipeline — Apache Airflow

## 1. Project Overview

This project demonstrates the orchestration of a lightweight Premier League data ingestion pipeline using Apache Airflow.

The pipeline retrieves match information from the football-data.org API and stores the response locally as a JSON file. Airflow manages execution scheduling, conditional execution, retries and failure alert logging.

## 2. Architecture

```text
       football-data.org API
                 |
                 v
        Python Extraction Script
          (extract_matches.py)
                 |
                 v
          Apache Airflow DAG
                 |
          Weekend Time Check
                 |
                 v
         Premier League Data
                 |
                 v
          data/matches.json
```

## 3. Technologies

- Python 3.12
- Apache Airflow 2.10.5
- REST API
- Requests
- Python-dotenv
- WSL Ubuntu
- JSON

## 4. Pipeline Workflow

1. Airflow checks the configured execution window.
2. The `ShortCircuitOperator` determines whether extraction is permitted.
3. The Python extraction function connects to the football-data.org API.
4. Match data is retrieved and saved as `data/matches.json`.
5. Airflow monitors task execution and handles failures.

## 5. Scheduling and Conditional Execution

The DAG runs hourly using the cron schedule:

```python
schedule="0 * * * *"
```

Extraction is permitted during the following window:

- Friday from 8:00 PM
- All Saturday
- All Sunday
- All Monday

Timezone: `Africa/Lagos`.

Manual DAG runs are permitted for testing.

## 6. Retry Configuration

The production DAG uses Airflow's retry mechanism to handle temporary task failures.

```python
default_args = {
    "owner": "airflow",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}
```

**Retry behaviour:**

- Initial execution: 1 attempt
- Maximum retries: 2
- Maximum total attempts: 3
- Retry delay: 5 minutes

This helps the pipeline recover from temporary API or network failures.

## 7. Failure Alerting

A custom failure callback named `failure_alert()` is attached to the extraction task.

When the task exhausts its retries and reaches final failure, the callback:

1. Retrieves the failed task and DAG identifiers.
2. Captures the exception message.
3. Writes an error message to the Airflow task logs.
4. Appends the alert to:

```text
logs/failure_alerts.log
```

Example alert:

```text
ALERT: Task extract_premier_league_matches failed
in DAG epl_weekend_ingestion.
Error: API connection failure
```

**Note:** This implementation uses local file-based alert logging. Email, SMS and Slack notifications are not configured.

## 8. Reliability Testing

A temporary test DAG was created to simulate an API failure.

The test verified:

- Automatic retries.
- Final task failure handling.
- Execution of the failure callback.
- Alert generation in the local log file.

The test DAG was removed after verification. The production DAG remains active.

## 9. Project Structure

```text
epl-weekend-airflow/
│
├── dags/
│   └── epl_weekend_ingestion.py
│
├── scripts/
│   └── extract_matches.py
│
├── data/
│   └── matches.json
│
├── logs/
│   └── failure_alerts.log
│
├── airflow_home/
├── airflow_venv/
├── .env
├── .gitignore
└── README.md
```

## 10. Running the Project

Activate the Python virtual environment:

```bash
source airflow_venv/bin/activate
```

Configure Airflow:

```bash
export AIRFLOW_HOME="$PWD/airflow_home"
export AIRFLOW__CORE__EXECUTOR=SequentialExecutor
export AIRFLOW__CORE__LOAD_EXAMPLES=False
export AIRFLOW__CORE__DAGS_FOLDER="$PWD/dags"
```

Start the scheduler:

```bash
airflow scheduler
```

In another terminal, activate the same environment and start the webserver:

```bash
airflow webserver --port 8080
```

Access the Airflow interface at:

```text
http://localhost:8080
```

## 11. Security

API credentials are stored in the `.env` file and excluded from Git through `.gitignore`.

The API token should never be committed to a public repository.

## 12. Learning Outcomes

This project demonstrates practical experience with:

- Apache Airflow DAG development.
- Python-based API ingestion.
- Scheduled and conditional task execution.
- Task dependency management.
- Automatic retries.
- Failure callbacks and alert logging.
- Basic pipeline reliability and monitoring.
