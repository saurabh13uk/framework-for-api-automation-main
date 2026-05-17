
## Approach

This framework of API automation strategy should cover the most important contract first, then grow toward deeper workflow coverage as risk increases.

## Test Strategy

- Validated API availability through status code checks.
- Validated response schema by checking required keys on every returned post.
- Validated response shape and data type before making assumptions about contents.
- Used fixtures for shared setup, so endpoint and client configuration stay centralized.
- Used parametrization for repeated contract checks and cleaner failure reporting.
- Saved sample response data as an execution artifact for debugging and downstream validation.

## Reporting Strategy

- Used terminal pytest output for fast local feedback.
- Used JUnit XML for CI systems.
- Used pytest HTML reports for human-readable evidence during reviews.

## Maintainability

- Keep endpoint paths in one place.
- Keep environment settings outside tests.
- Keep API client methods reusable and thin.
- Add new API resources as new client methods and test modules.
- Avoid hard-coded response assumptions unless they are part of the API contract.

## CI/CD Recommendation

Run this suite on every pull request and nightly against the public API. In a production API program, separate smoke, regression, and contract tests so failures are easier to triage.

