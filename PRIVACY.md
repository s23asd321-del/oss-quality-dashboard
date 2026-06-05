# Privacy

`oss-quality-dashboard` is designed for local-first use.

- It does not access the network by default.
- It does not upload files.
- It does not collect telemetry.
- Scan results are stored in local SQLite at `data/oss_quality_dashboard.sqlite` by default.
- Users can delete local scan data by deleting the local database file.

Reports may include project names and relative file paths. They may also include a redacted local path. Review reports before sharing them publicly, especially for private repositories or internal project names.

