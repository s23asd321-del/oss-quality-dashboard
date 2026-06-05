# Scoring Model

Each scan starts at 100 points.

| Severity | Penalty |
| --- | --- |
| error | -10 |
| warning | -4 |
| info | 0 |

Scores cannot go below 0.

## Grades

| Score | Grade |
| --- | --- |
| 90-100 | strong |
| 70-89 | good |
| 50-69 | needs work |
| 0-49 | risky |

## Limitations

The score is only a heuristic reference. It does not represent:

- Security assurance
- Legal review
- Privacy compliance
- Secret scanning
- Vulnerability scanning
- Project value
- Maintainer skill level
- Public release readiness

The model is intentionally simple so users can understand why a repository received a score.

