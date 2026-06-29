#!/usr/bin/env python3
"""Audit subgroup/coset domain-convention language across the TeX sources.

The blueprint's M0 note records a convention drift: Papers A and B are written
mostly for multiplicative subgroups, while Paper D allows multiplicative cosets.
This script does not edit stable papers.  It reports where subgroup/coset
language appears and extracts likely convention-setting lines for maintainer
review.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path


STATUS = "AUDIT"
THEOREM_ID = "tex/proximity_blueprint_v3.tex:M0 domain convention drift"
OBJECT = "Subgroup/coset domain-convention audit"
SOURCE_FILES = (
    "tex/RS_disproof_v3.tex",
    "tex/slackMCA_v3.tex",
    "tex/cs25_cap_v4.tex",
    "tex/snarks_v4.tex",
    "tex/proximity_blueprint_v3.tex",
)

CONVENTION_HINTS = (
    "evaluation domain",
    "subgroup case",
    "subgroup domain",
    "subgroup domains",
    "multiplicative coset",
    "coset convention",
    "subgroups while",
    "allows multiplicative cosets",
    "D\\le",
    "D\\subseteq",
    "D=\\alpha H",
    "H\\le",
)


def compact(line: str) -> str:
    return " ".join(line.strip().split())


def row_kind(text: str) -> str:
    lower = text.lower()
    has_subgroup = "subgroup" in lower
    has_coset = "coset" in lower
    if has_subgroup and has_coset:
        return "both"
    if has_coset:
        return "coset"
    if has_subgroup:
        return "subgroup"
    return "other"


def is_convention_candidate(text: str) -> bool:
    return any(hint in text for hint in CONVENTION_HINTS)


def scan_file(root: Path, relative: str) -> list[dict[str, object]]:
    path = root / relative
    rows: list[dict[str, object]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        text = compact(line)
        if "subgroup" not in text.lower() and "coset" not in text.lower():
            continue
        rows.append(
            {
                "file": relative,
                "line": number,
                "kind": row_kind(text),
                "convention_candidate": is_convention_candidate(text),
                "excerpt": text[:220],
            }
        )
    return rows


def scan(root: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for relative in SOURCE_FILES:
        rows.extend(scan_file(root, relative))
    return rows


def payload(rows: list[dict[str, object]]) -> dict[str, object]:
    by_file: dict[str, Counter[str]] = defaultdict(Counter)
    by_kind = Counter(str(row["kind"]) for row in rows)
    convention_rows = [row for row in rows if row["convention_candidate"]]
    for row in rows:
        by_file[str(row["file"])][str(row["kind"])] += 1
    paper_a_subgroup = by_file["tex/RS_disproof_v3.tex"]["subgroup"]
    paper_d_coset = by_file["tex/cs25_cap_v4.tex"]["coset"]
    blueprint_mentions_drift = any(
        row["file"] == "tex/proximity_blueprint_v3.tex"
        and row["convention_candidate"]
        and row["kind"] == "both"
        for row in rows
    )
    return {
        "status": STATUS,
        "theorem_id": THEOREM_ID,
        "object": OBJECT,
        "inputs": {
            "source_files": list(SOURCE_FILES),
            "convention_hints": list(CONVENTION_HINTS),
        },
        "result": {
            "counts_by_kind": dict(sorted(by_kind.items())),
            "counts_by_file": {
                file_name: dict(sorted(counter.items()))
                for file_name, counter in sorted(by_file.items())
            },
            "convention_candidate_count": len(convention_rows),
            "drift_signal": {
                "paper_a_subgroup_rows": paper_a_subgroup,
                "paper_d_coset_rows": paper_d_coset,
                "blueprint_mentions_drift": blueprint_mentions_drift,
                "detected": paper_a_subgroup > 0
                and paper_d_coset > 0
                and blueprint_mentions_drift,
            },
            "convention_rows": convention_rows,
        },
    }


def print_text(cert: dict[str, object]) -> None:
    result = cert["result"]
    print(OBJECT)
    print(f"Status: {STATUS}")
    print(f"Theorem/problem ID: {THEOREM_ID}")
    print("Object checked: subgroup/coset convention language.")
    print()
    print("Counts by kind:")
    for kind, count in result["counts_by_kind"].items():
        print(f"- {kind}: {count}")
    print()
    print("Counts by file:")
    for file_name, counts in result["counts_by_file"].items():
        formatted = ", ".join(f"{key}={value}" for key, value in counts.items())
        print(f"- {file_name}: {formatted}")
    print()
    print("Drift signal:")
    for key, value in result["drift_signal"].items():
        print(f"- {key}: {value}")
    print()
    print("Convention candidates:")
    for row in result["convention_rows"]:
        print(
            "{file}:{line}: [{kind}] {excerpt}".format(
                file=row["file"],
                line=row["line"],
                kind=row["kind"],
                excerpt=row["excerpt"],
            )
        )


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
