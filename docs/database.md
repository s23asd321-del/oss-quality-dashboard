# Database

The default SQLite path is:

```text
data/oss_quality_dashboard.sqlite
```

The app creates `data/` when the database connection is opened.

## projects

| Field | Type | Notes |
| --- | --- | --- |
| id | INTEGER | Primary key |
| name | TEXT | Display name |
| path | TEXT | User-specified project directory, stored after resolution |
| created_at | TEXT | ISO timestamp |
| updated_at | TEXT | ISO timestamp |

The `projects.path` value is protected by a unique index so the same resolved local directory is not added multiple times.

## scans

| Field | Type | Notes |
| --- | --- | --- |
| id | INTEGER | Primary key |
| project_id | INTEGER | References `projects.id` with cascade delete |
| started_at | TEXT | ISO timestamp |
| finished_at | TEXT | ISO timestamp, nullable during running scan |
| status | TEXT | `running`, `finished`, or future status values |
| score | INTEGER | Heuristic score |
| summary_json | TEXT | JSON string with score, grade, counts, and scanner summary |

## findings

| Field | Type | Notes |
| --- | --- | --- |
| id | INTEGER | Primary key |
| scan_id | INTEGER | References `scans.id` with cascade delete |
| rule_id | TEXT | Rule identifier |
| severity | TEXT | `info`, `warning`, or `error` |
| title | TEXT | Short finding title |
| message | TEXT | Finding explanation |
| path | TEXT | Relative path or logical location |
| recommendation | TEXT | Conservative next step |
| created_at | TEXT | ISO timestamp |

## Delete Local Data

Stop the app, then remove:

```text
data/oss_quality_dashboard.sqlite
```

This deletes local scan history only. It does not modify scanned repositories.
