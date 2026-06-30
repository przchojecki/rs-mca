#!/usr/bin/env python3
"""Audit BCIKS bibliography-key drift across the TeX sources.

The blueprint notes one known drift: Paper A keys the foundational proximity
reference as `BCIKS23`, while the other manuscripts use `BCIKS20`.  This script
does not edit stable papers.  It reports where BCIKS-style keys are cited and
where their `bibitem`s are declared, so a maintainer can normalize the key when
stable TeX edits are in scope.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


STATUS = "AUDIT"
THEOREM_ID = "tex/proximity_blueprint_v3.tex:M0 bibkey drift"
OBJECT = "BCIKS bibliography-key drift audit"
SOURCE_FILES = (
    "tex/RS_disproof_v3.tex",
    "tex/slackMCA_v3.tex",
    "tex/cs25_cap_v4.tex",
    "tex/snarks_v4.tex",
    "tex/proximity_blueprint_v3.tex",
)
WATCH_PREFIX = "BCIKS"
CITE_RE = re.compile(r"\\cite(?:\[[^\]]*\])*{([^}]*)}")
BIBITEM_RE = re.compile(r"\\bibitem{([^}]*)}")


def split_keys(raw: str) -> list[str]:
    return [key.strip() for key in raw.split(",") if key.strip()]


def scan_file(root: Path, relative: str) -> list[dict[str, object]]:
    path = root / relative
    rows: list[dict[str, object]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        for match in CITE_RE.finditer(line):
            for key in split_keys(match.group(1)):
                if key.startswith(WATCH_PREFIX):
                    rows.append(
                        {
                            "file": relative,
                            "line": number,
                            "kind": "cite",
                            "key": key,
                            "excerpt": " ".join(line.strip().split()),
                        }
                    )
        for match in BIBITEM_RE.finditer(line):
            key = match.group(1)
            if key.startswith(WATCH_PREFIX):
                rows.append(
                    {
                        "file": relative,
                        "line": number,
                        "kind": "bibitem",
                        "key": key,
                        "excerpt": " ".join(line.strip().split()),
                    }
                )
    return rows


def scan(root: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for relative in SOURCE_FILES:
        rows.extend(scan_file(root, relative))
    return rows


def payload(rows: list[dict[str, object]]) -> dict[str, object]:
    by_key = Counter(str(row["key"]) for row in rows)
    by_file: dict[str, Counter[str]] = defaultdict(Counter)
    declared: dict[str, list[str]] = defaultdict(list)
    cited: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        file_name = str(row["file"])
        key = str(row["key"])
        by_file[file_name][key] += 1
        if row["kind"] == "bibitem":
            declared[key].append(file_name)
        if row["kind"] == "cite":
            cited[key].append(file_name)
    return {
        "status": STATUS,
        "theorem_id": THEOREM_ID,
        "object": OBJECT,
        "inputs": {
            "source_files": list(SOURCE_FILES),
            "watch_prefix": WATCH_PREFIX,
        },
        "result": {
            "keys_seen": sorted(by_key),
            "counts_by_key": dict(sorted(by_key.items())),
            "counts_by_file": {
                file_name: dict(sorted(counter.items()))
                for file_name, counter in sorted(by_file.items())
            },
            "bibitems_by_key": {
                key: sorted(set(files)) for key, files in sorted(declared.items())
            },
            "citations_by_key": {
                key: sorted(set(files)) for key, files in sorted(cited.items())
            },
            "drift_detected": len(by_key) > 1,
            "rows": rows,
        },
    }


def print_text(cert: dict[str, object]) -> None:
    result = cert["result"]
    print(OBJECT)
    print(f"Status: {STATUS}")
    print(f"Theorem/problem ID: {THEOREM_ID}")
    print("Object checked: BCIKS-style citation keys and bibitems.")
    print()
    print(f"Keys seen: {', '.join(result['keys_seen'])}")
    print(f"Drift detected: {result['drift_detected']}")
    print()
    print("Counts by key:")
    for key, count in result["counts_by_key"].items():
        print(f"- {key}: {count}")
    print()
    print("Counts by file:")
    for file_name, counts in result["counts_by_file"].items():
        formatted = ", ".join(f"{key}={count}" for key, count in counts.items())
        print(f"- {file_name}: {formatted}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format. JSON is machine-readable and text is for review.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(__file__).resolve().parents[2]
    cert = payload(scan(root))
    if args.format == "json":
        print(json.dumps(cert, indent=2, sort_keys=True))
    else:
        print_text(cert)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
