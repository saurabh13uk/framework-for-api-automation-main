# JSONPlaceholder API Automation Framework

Python API automation framework using `requests`, `pytest`, and Postman validation scripts for:

`https://jsonplaceholder.typicode.com/posts`

## What This Framework Covers

- Fetches all posts from the public API.
- Validates HTTP status code `200`.
- Verifies every post contains `userId`, `id`, `title`, and `body`.
- Saves the first 5 posts into a local JSON file.
- Provides pytest fixtures, parametrized tests, and optional HTML/JUnit reporting.
- Includes a Postman collection with validation scripts.


## Project Structure

```text
api_automation_framework/
  api/
    client.py
    endpoints.py
  config/
    settings.py
  utils/
    file_writer.py
    api_reporter.py
    logger.py
  scripts/
    fetch_and_save_posts.py
  tests/
    conftest.py
    test_posts_api.py
  postman/
    jsonplaceholder_posts_collection.json
  data/
    .gitkeep
  reports/
    .gitkeep
  requirements.txt
  .gitignore
  pytest.ini
  pyproject.toml
  README.md
  QA_STRATEGY.md
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the Python Script

```bash
python scripts/fetch_and_save_posts.py
```

Output file:

```text
data/first_5_posts.json
```

## Run Tests

```bash
pytest
```

Run with reports:

```bash
pytest --html=reports/api_report.html --self-contained-html --junitxml=reports/junit.xml
```
## Logs in Reports
The framework captures API execution logs during pytest runs and writes them to:

```text
logs/api_automation.log
```
The same log lines are also displayed inside the custom API execution report:

```text
reports/api_execution_report.html
reports/api_execution_report.json
```

Each report entry includes request details, response details, status code, response time, and logs for that API call.

## Import in IDE

Open this folder directly in PyCharm, VS Code, or another IDE:

```text
/Users/admin/Download/build-a-framework-for-api-automation
```

Set the interpreter to your virtual environment and run either:

- `scripts/fetch_and_save_posts.py`
- `tests/test_posts_api.py`

