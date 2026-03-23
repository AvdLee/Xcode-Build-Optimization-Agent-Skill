# Recommendation Format

All optimization skills should report recommendations in a shared structure so the orchestrator can merge and prioritize them cleanly.

## Required Fields

Each recommendation should include:

- `title`
- `wait_time_impact` -- plain-language statement of expected wall-clock impact, e.g. "Expected to reduce your clean build by ~3s", "Reduces parallel compile work but unlikely to reduce build wait time", or "Impact on wait time is uncertain -- re-benchmark to confirm"
- `category`
- `observed_evidence`
- `estimated_impact`
- `confidence`
- `approval_required`
- `benchmark_verification_status`

## Suggested Optional Fields

- `scope`
- `affected_files`
- `affected_targets`
- `affected_packages`
- `implementation_notes`
- `risk_level`

## JSON Example

```json
{
  "recommendations": [
    {
      "title": "Guard a release-only symbol upload script",
      "wait_time_impact": "Expected to reduce your incremental build by approximately 6 seconds.",
      "category": "project",
      "observed_evidence": [
        "Incremental builds spend 6.3 seconds in a run script phase.",
        "The script runs for Debug builds even though the output is only needed in Release."
      ],
      "estimated_impact": "High incremental-build improvement",
      "confidence": "High",
      "approval_required": true,
      "benchmark_verification_status": "Not yet verified",
      "scope": "Target build phase",
      "risk_level": "Low"
    }
  ]
}
```

## Markdown Rendering Guidance

When rendering for human review, preserve the same field order:

1. title
2. wait-time impact
3. observed evidence
4. estimated impact
5. confidence
6. approval required
7. benchmark verification status

That makes it easier for the developer to approve or reject specific items quickly.

## Verification Status Values

Recommended values:

- `Not yet verified`
- `Queued for verification`
- `Verified improvement`
- `No measurable improvement`
- `Inconclusive due to benchmark noise`
