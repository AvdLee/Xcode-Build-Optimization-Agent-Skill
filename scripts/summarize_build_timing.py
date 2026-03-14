#!/usr/bin/env python3

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Optional

_TASK_COUNT_RE = re.compile(r"^(.+?)\s*\((\d+)\s+tasks?\)$")


def _extract_task_count(name: str) -> tuple[str, Optional[int]]:
    """Split 'Category (N tasks)' into ('Category', N)."""
    match = _TASK_COUNT_RE.match(name)
    if match:
        return match.group(1).strip(), int(match.group(2))
    return name, None


def parse_timing_summary(output: str) -> List[Dict]:
    categories: Dict[str, float] = {}
    task_counts: Dict[str, Optional[int]] = {}
    for raw_line in output.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        for suffix in (" seconds", " second", " sec"):
            if not line.endswith(suffix):
                continue
            trimmed = line[: -len(suffix)]
            if "|" in trimmed:
                name_part, _, seconds_text = trimmed.rpartition("|")
            else:
                name_part, _, seconds_text = trimmed.rpartition(" ")
            try:
                seconds = float(seconds_text.strip())
            except ValueError:
                continue
            cleaned_name = name_part.replace("  ", " ").strip(" -:")
            if len(cleaned_name) < 3:
                continue
            base_name, count = _extract_task_count(cleaned_name)
            categories[base_name] = categories.get(base_name, 0.0) + seconds
            if count is not None:
                task_counts[base_name] = (task_counts.get(base_name) or 0) + count
            break
    result: List[Dict] = []
    for name, seconds in sorted(categories.items(), key=lambda item: item[1], reverse=True):
        entry: Dict = {"name": name, "seconds": round(seconds, 3)}
        if name in task_counts:
            entry["task_count"] = task_counts[name]
        result.append(entry)
    return result


def summarize_json(path: Path, top: int) -> str:
    payload = json.loads(path.read_text())
    sections = []
    for build_type in ("clean", "incremental"):
        aggregate: Dict[str, float] = {}
        for run in payload.get("runs", {}).get(build_type, []):
            for category in run.get("timing_summary_categories", []):
                aggregate[category["name"]] = aggregate.get(category["name"], 0.0) + category["seconds"]
        ranked = sorted(aggregate.items(), key=lambda item: item[1], reverse=True)[:top]
        sections.append(f"{build_type.title()} top categories:")
        if not ranked:
            sections.append("  (no parsed timing summary categories)")
        else:
            for name, seconds in ranked:
                sections.append(f"  - {name}: {seconds:.3f}s total")
    return "\n".join(sections)


def summarize_log(path: Path, top: int) -> str:
    categories = parse_timing_summary(path.read_text())[:top]
    if not categories:
        return "No timing summary categories detected."
    lines = ["Top timing summary categories:"]
    for category in categories:
        lines.append(f"  - {category['name']}: {category['seconds']:.3f}s")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize Xcode build timing output.")
    parser.add_argument("input", help="Path to a benchmark JSON artifact or raw xcodebuild log")
    parser.add_argument("--top", type=int, default=5, help="Number of categories to display")
    args = parser.parse_args()

    path = Path(args.input)
    if path.suffix == ".json":
        print(summarize_json(path, args.top))
    else:
        print(summarize_log(path, args.top))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
