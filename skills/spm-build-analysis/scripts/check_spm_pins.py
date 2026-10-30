#!/usr/bin/env python3

"""Scan a project.xcproj or project.pbxproj for branch-pinned SPM dependencies and check tag availability."""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


_PKG_REF_RE = re.compile(
    r"(/\*\s*XCRemoteSwiftPackageReference\s+\"(?P<name>[^\"]+)\"\s*\*/\s*=\s*\{[^}]*?"
    r"repositoryURL\s*=\s*\"(?P<url>[^\"]+)\"[^}]*?"
    r"requirement\s*=\s*\{(?P<req>[^}]*)\})",
    re.DOTALL,
)

_KIND_RE = re.compile(r"kind\s*=\s*(\w+)\s*;")
_BRANCH_RE = re.compile(r"branch\s*=\s*(\w+)\s*;")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check branch-pinned SPM dependencies for available tags."
    )
    parser.add_argument(
        "--project",
        required=True,
        help="Path to the .xcodeproj directory",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON",
    )
    return parser.parse_args()


def find_branch_pins(pbxproj: str) -> List[Dict[str, str]]:
    results: List[Dict[str, str]] = []
    for match in _PKG_REF_RE.finditer(pbxproj):
        name = match.group("name")
        url = match.group("url")
        req = match.group("req")
        kind_match = _KIND_RE.search(req)
        if not kind_match:
            continue
        kind = kind_match.group(1)
        if kind != "branch":
            continue
        branch_match = _BRANCH_RE.search(req)
        branch = branch_match.group(1) if branch_match else "unknown"
        results.append({"name": name, "url": url, "branch": branch})
    return results


def _load_json5(text: str) -> Any:
    """Parse the JSON5 subset Xcode writes: standard JSON plus comments and trailing commas."""
    out: List[str] = []
    i, n = 0, len(text)
    in_string = False
    while i < n:
        c = text[i]
        if in_string:
            out.append(c)
            if c == "\\" and i + 1 < n:
                out.append(text[i + 1])
                i += 2
                continue
            if c == '"':
                in_string = False
            i += 1
            continue
        if c == '"':
            in_string = True
        elif text.startswith("//", i):
            end = text.find("\n", i)
            i = n if end == -1 else end
            continue
        elif text.startswith("/*", i):
            end = text.find("*/", i + 2)
            i = n if end == -1 else end + 2
            continue
        elif c in "]}":
            k = len(out) - 1
            while k >= 0 and out[k].isspace():
                k -= 1
            if k >= 0 and out[k] == ",":
                del out[k]
        out.append(c)
        i += 1
    return json.loads("".join(out))


def find_branch_pins_xcproj(xcproj: str) -> List[Dict[str, str]]:
    results: List[Dict[str, str]] = []
    for package in _load_json5(xcproj).get("packages", []):
        if package.get("kind") != "remote":
            continue
        version = package.get("version") or {}
        if "branch" not in version:
            continue
        url = package["repository"]
        name = url.rstrip("/").rsplit("/", 1)[-1]
        if name.endswith(".git"):
            name = name[: -len(".git")]
        results.append({"name": name, "url": url, "branch": version["branch"]})
    return results


def check_tags(url: str) -> List[str]:
    try:
        result = subprocess.run(
            ["git", "ls-remote", "--tags", url],
            capture_output=True,
            text=True,
            timeout=15,
        )
        if result.returncode != 0:
            return []
        tags: List[str] = []
        for line in result.stdout.strip().splitlines():
            ref = line.split("\t")[-1] if "\t" in line else ""
            if ref.startswith("refs/tags/") and not ref.endswith("^{}"):
                tags.append(ref.replace("refs/tags/", ""))
        return tags
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return []


def main() -> int:
    args = parse_args()
    xcproj_path = Path(args.project) / "project.xcproj"
    pbxproj_path = Path(args.project) / "project.pbxproj"
    if xcproj_path.exists():
        pins = find_branch_pins_xcproj(xcproj_path.read_text())
    elif pbxproj_path.exists():
        pins = find_branch_pins(pbxproj_path.read_text())
    else:
        sys.stderr.write(f"Not found: {xcproj_path} or {pbxproj_path}\n")
        return 1

    if not pins:
        print("No branch-pinned SPM dependencies found.")
        return 0

    results: List[Dict] = []
    for pin in pins:
        tags = check_tags(pin["url"])
        entry = {
            "name": pin["name"],
            "url": pin["url"],
            "branch": pin["branch"],
            "tags_available": len(tags) > 0,
            "latest_tags": tags[-5:] if tags else [],
        }
        results.append(entry)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for r in results:
            status = "tags available" if r["tags_available"] else "no tags (pin to revision)"
            latest = f" (latest: {', '.join(r['latest_tags'])})" if r["latest_tags"] else ""
            print(f"  {r['name']}: branch={r['branch']} -> {status}{latest}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
