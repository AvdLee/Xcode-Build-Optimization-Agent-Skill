#!/usr/bin/env python3

import argparse
import json
from pathlib import Path


FIELD_LABELS = [
    ("category", "Category"),
    ("observed_evidence", "Observed evidence"),
    ("estimated_impact", "Estimated impact"),
    ("confidence", "Confidence"),
    ("approval_required", "Approval required"),
    ("benchmark_verification_status", "Benchmark verification status"),
    ("scope", "Scope"),
    ("risk_level", "Risk level"),
]


def render_recommendation(item: dict, index: int) -> str:
    lines = [f"## {index}. {item.get('title', 'Untitled recommendation')}"]
    for key, label in FIELD_LABELS:
        value = item.get(key)
        if value is None:
            continue
        if isinstance(value, list):
            lines.append(f"**{label}:**")
            for entry in value:
                lines.append(f"- {entry}")
            continue
        lines.append(f"**{label}:** {value}")
    if item.get("implementation_notes"):
        lines.append("**Implementation notes:**")
        for entry in item["implementation_notes"]:
            lines.append(f"- {entry}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render recommendation JSON as Markdown.")
    parser.add_argument("input", help="Path to a recommendation JSON file")
    parser.add_argument("--output", help="Optional output Markdown path")
    args = parser.parse_args()

    payload = json.loads(Path(args.input).read_text())
    recommendations = payload.get("recommendations", [])
    sections = ["# Xcode Build Recommendations", ""]
    for index, item in enumerate(recommendations, start=1):
        sections.append(render_recommendation(item, index))
        sections.append("")
    markdown = "\n".join(sections).rstrip() + "\n"

    if args.output:
        Path(args.output).write_text(markdown)
    else:
        print(markdown, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
