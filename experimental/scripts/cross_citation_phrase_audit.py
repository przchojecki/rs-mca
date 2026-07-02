#!/usr/bin/env python3
"""Audit companion-style cross-citation phrases in the TeX sources.

This supports `agents.md` A2: when a manuscript says a companion proves
something, future edits should replace that prose with a theorem,
proposition, lemma, or corollary reference where possible.

The script is intentionally conservative.  It does not edit stable papers and
does not decide correctness.  It only classifies lines containing
companion-style phrases as:

* `pinned`: same line has an apparent theorem/proposition/corollary/lemma pin;
* `numbering_not_frozen`: source explicitly says printed theorem names are used;
* `review`: proof-bearing companion prose without an obvious same-line pin;
* `context`: companion prose that appears not to assert a theorem dependency.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


STATUS = "AUDIT"
THEOREM_ID = "agents.md:A2"
OBJECT = "Cross-citation phrase audit"

SOURCE_FILES = (
    "tex/RS_disproof_v3.tex",
    "tex/slackMCA_v4.tex",
    "tex/cs25_cap_v12.tex",
    "tex/snarks_v5.tex",
    "tex/proximity_blueprint_v3.tex",
)

WATCH_TERMS = (
    "companion",
    "companion's",
    "companion cap paper",
    "companion manuscript",
    "printed theorem names rather than numbers",
)

PROOF_TERMS = (
    "prove",
    "proves",
    "proved",
    "theorem",
    "theorem-backed",
    "results",
    "universal cap",
    "cap paper",
    "special lanes",
    "challenge cap",
    "subfield-confinement",
)

PIN_TERMS = (
    "\\cite[Thm.",
    "\\cite[Prop.",
    "\\cite[Cor.",
    "\\cite[Lem.",
    "\\cref{",
    "\\Cref{",
    "Main Thm",
    "main theorem",
    "Theorem",
    "Proposition",
    "Corollary",
    "Lemma",
)

IGNORE_TERMS = (
    "companion bibliography",
    "Stale companion bibitem",
    "companion manuscript,",
)


def contains_any(line: str, terms: tuple[str, ...]) -> bool:
    return any(term in line for term in terms)


def classify(line: str) -> str:
    if line.strip().startswith("\\begin"):
        return "context"
    if "printed theorem names rather than numbers" in line:
        return "numbering_not_frozen"
    if not contains_any(line, PROOF_TERMS):
        return "context"
    if contains_any(line, PIN_TERMS):
        return "pinned"
    return "review"


def excerpt(line: str, width: int = 180) -> str:
    compact = " ".join(line.strip().split())
    if len(compact) <= width:
        return compact
    return compact[: width - 3] + "..."


def scan(root: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for relative in SOURCE_FILES:
        path = root / relative
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if contains_any(line, IGNORE_TERMS):
                continue
            if not contains_any(line, WATCH_TERMS):
                continue
            rows.append(
                {
                    "file": relative,
                    "line": number,
                    "classification": classify(line),
                    "excerpt": excerpt(line),
                }
            )
    return rows


def payload(rows: list[dict[str, object]]) -> dict[str, object]:
    counts = Counter(str(row["classification"]) for row in rows)
    return {
        "status": STATUS,
        "theorem_id": THEOREM_ID,
        "object": OBJECT,
        "inputs": {
            "source_files": list(SOURCE_FILES),
            "watch_terms": list(WATCH_TERMS),
            "pin_terms": list(PIN_TERMS),
        },
        "result": {
            "counts": dict(sorted(counts.items())),
            "rows": rows,
            "review_rows": [
                row for row in rows if row["classification"] == "review"
            ],
        },
    }


def print_text(cert: dict[str, object]) -> None:
    result = cert["result"]
    print(OBJECT)
    print(f"Status: {STATUS}")
    print(f"Theorem/problem ID: {THEOREM_ID}")
    print("Object checked: companion-style cross-citation phrases.")
    print()
    print("Counts:")
    for name, count in result["counts"].items():
        print(f"- {name}: {count}")
    print()
    print("Rows needing review:")
    for row in result["review_rows"]:
        print(
            "{file}:{line}: {excerpt}".format(
                file=row["file"],
                line=row["line"],
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
