#!/usr/bin/env python3
"""Audit Paper C security-mode label coverage.

Proof status: AUDIT.

The blueprint asks Paper C to label parameter sets as theorem-backed,
conjectural aggressive, obstruction-audit, or hybrid.  This script is a
deterministic text audit: it does not edit the manuscripts and does not prove
soundness.  It records where the labels already appear and where a stricter
"mode" label is absent.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


SOURCE_FILES = (
    "tex/snarks_v4.tex",
    "tex/proximity_blueprint_v3.tex",
)
PAPER_C_FILE = "tex/snarks_v4.tex"
BLUEPRINT_FILE = "tex/proximity_blueprint_v3.tex"
PROBLEM_ID = "Paper C C5 / blueprint item: Security statement modes"
PROOF_STATUS = "AUDIT"


MODE_PATTERNS = {
    "theorem-backed": {
        "strict": (r"\btheorem-backed(?: certificate)? mode\b",),
        "loose": (r"\btheorem-backed\b",),
    },
    "conjectural aggressive": {
        "strict": (r"\bconjectural aggressive mode\b",),
        "loose": (
            r"\bconjectural aggressive\b",
            r"\bconjectural with explicit named assumptions\b",
            r"\bconjectural corrected route\b",
            r"\bconjectural assumptions\b",
        ),
    },
    "obstruction-audit": {
        "strict": (r"\bobstruction-audit mode\b",),
        "loose": (r"\bobstruction-audit\b", r"\bobstruction audit\b"),
    },
    "hybrid": {
        "strict": (r"\bhybrid mode\b",),
        "loose": (
            r"\bhybrid schedule\b",
            r"\bhybrid schedules\b",
            r"\bextension hybrids\b",
            r"\bhybrid\b",
        ),
    },
}

REQUIREMENT_PATTERNS = (
    "Security statement modes",
    "Choose theorem mode",
    "Proof-status hygiene",
)


@dataclass(frozen=True)
class Hit:
    file: str
    line: int
    mode: str
    match_kind: str
    matched_text: str
    snippet: str


@dataclass(frozen=True)
class RequirementLine:
    file: str
    line: int
    marker: str
    snippet: str


@dataclass(frozen=True)
class SectionHeading:
    file: str
    line: int
    heading: str
    matched_mode: str | None


@dataclass(frozen=True)
class ParameterRow:
    file: str
    line: int
    row: str
    inline_mode_hits: tuple[str, ...]
    nearby_caption_hint: str | None


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_lines(root: Path, relative_path: str) -> list[str]:
    return (root / relative_path).read_text(encoding="utf-8").splitlines()


def clean_snippet(line: str) -> str:
    return re.sub(r"\s+", " ", line.strip())


def iter_matches(line: str, patterns: Iterable[str]) -> Iterable[tuple[str, str]]:
    for pattern in patterns:
        for match in re.finditer(pattern, line, flags=re.IGNORECASE):
            yield pattern, match.group(0)


def collect_hits(root: Path) -> list[Hit]:
    hits: list[Hit] = []
    seen: set[tuple[str, str, int, str, str]] = set()
    for relative_path in SOURCE_FILES:
        for line_no, line in enumerate(read_lines(root, relative_path), start=1):
            for mode, kinds in MODE_PATTERNS.items():
                for match_kind, patterns in kinds.items():
                    for _pattern, matched_text in iter_matches(line, patterns):
                        key = (
                            relative_path,
                            mode,
                            line_no,
                            match_kind,
                            matched_text.lower(),
                        )
                        if key in seen:
                            continue
                        seen.add(key)
                        hits.append(
                            Hit(
                                file=relative_path,
                                line=line_no,
                                mode=mode,
                                match_kind=match_kind,
                                matched_text=matched_text,
                                snippet=clean_snippet(line),
                            )
                        )
    return hits


def collect_requirements(root: Path) -> list[RequirementLine]:
    requirements: list[RequirementLine] = []
    for line_no, line in enumerate(read_lines(root, BLUEPRINT_FILE), start=1):
        for marker in REQUIREMENT_PATTERNS:
            if marker.lower() in line.lower():
                requirements.append(
                    RequirementLine(
                        file=BLUEPRINT_FILE,
                        line=line_no,
                        marker=marker,
                        snippet=clean_snippet(line),
                    )
                )
    return requirements


def heading_mode(heading: str) -> str | None:
    lowered = heading.lower()
    for mode in MODE_PATTERNS:
        if mode in lowered:
            return mode
    if "theorem-backed certificate" in lowered:
        return "theorem-backed"
    return None


def collect_headings(root: Path) -> list[SectionHeading]:
    headings: list[SectionHeading] = []
    for line_no, line in enumerate(read_lines(root, PAPER_C_FILE), start=1):
        match = re.search(r"\\(?:sub)*section\{([^}]*)\}", line)
        if not match:
            continue
        heading = match.group(1)
        if "mode" in heading.lower() or "fallback" in heading.lower():
            headings.append(
                SectionHeading(
                    file=PAPER_C_FILE,
                    line=line_no,
                    heading=heading,
                    matched_mode=heading_mode(heading),
                )
            )
    return headings


def row_mode_hits(row: str) -> tuple[str, ...]:
    hits: list[str] = []
    for mode, kinds in MODE_PATTERNS.items():
        patterns = tuple(kinds["strict"]) + tuple(kinds["loose"])
        if any(re.search(pattern, row, flags=re.IGNORECASE) for pattern in patterns):
            hits.append(mode)
    return tuple(hits)


def caption_hint(row: str, caption: str) -> str | None:
    if "theorem-backed" in caption.lower():
        if "johnson" in row.lower() or "folded" in row.lower():
            return "caption says Johnson and folded rows are theorem-backed"
    if "conditional on" in caption.lower() and "corrected rs" in row.lower():
        return "caption says corrected rows are conditional on named assumptions"
    return None


def collect_parameter_rows(root: Path) -> list[ParameterRow]:
    lines = read_lines(root, PAPER_C_FILE)
    table_start = None
    table_end = None
    for index, line in enumerate(lines):
        if r"\label{tab:field-tradeoff}" in line:
            for back_index in range(index, -1, -1):
                if r"\begin{table}" in lines[back_index]:
                    table_start = back_index
                    break
            if table_start is None:
                table_start = index
        if table_start is not None and r"\end{table}" in line:
            table_end = index
            break
    if table_start is None or table_end is None:
        return []

    table_lines = lines[table_start : table_end + 1]
    caption = " ".join(clean_snippet(line) for line in table_lines if r"\caption{" in line)
    rows: list[ParameterRow] = []
    for offset, line in enumerate(table_lines, start=table_start + 1):
        stripped = clean_snippet(line)
        if "&" not in stripped or r"\\" not in stripped:
            continue
        if "Setting &" in stripped or "rule" in stripped:
            continue
        rows.append(
            ParameterRow(
                file=PAPER_C_FILE,
                line=offset,
                row=stripped,
                inline_mode_hits=row_mode_hits(stripped),
                nearby_caption_hint=caption_hint(stripped, caption),
            )
        )
    return rows


def summarize_modes(hits: list[Hit]) -> dict[str, dict[str, object]]:
    summary: dict[str, dict[str, object]] = {}
    for mode in MODE_PATTERNS:
        strict_paper_c = [
            hit for hit in hits
            if hit.file == PAPER_C_FILE and hit.mode == mode and hit.match_kind == "strict"
        ]
        loose_paper_c = [
            hit for hit in hits
            if hit.file == PAPER_C_FILE and hit.mode == mode and hit.match_kind == "loose"
        ]
        strict_blueprint = [
            hit for hit in hits
            if hit.file == BLUEPRINT_FILE and hit.mode == mode and hit.match_kind == "strict"
        ]
        loose_blueprint = [
            hit for hit in hits
            if hit.file == BLUEPRINT_FILE and hit.mode == mode and hit.match_kind == "loose"
        ]
        summary[mode] = {
            "strict_hits_in_paper_c": len(strict_paper_c),
            "loose_hits_in_paper_c": len(loose_paper_c),
            "strict_hits_in_blueprint": len(strict_blueprint),
            "loose_hits_in_blueprint": len(loose_blueprint),
            "strict_missing_in_paper_c": not strict_paper_c,
        }
    return summary


def build_notes(summary: dict[str, dict[str, object]], rows: list[ParameterRow]) -> list[str]:
    notes: list[str] = []
    strict_missing = [
        mode for mode, data in summary.items()
        if data["strict_missing_in_paper_c"]
    ]
    if strict_missing:
        notes.append(
            "Paper C lacks strict '<label> mode' phrasing for: "
            + ", ".join(strict_missing)
            + "."
        )
    implied_rows = [
        row for row in rows
        if not row.inline_mode_hits and row.nearby_caption_hint is not None
    ]
    if implied_rows:
        notes.append(
            "Some parameter rows rely on caption-level mode hints rather than inline labels."
        )
    if not rows:
        notes.append("The field-tradeoff parameter table was not located.")
    notes.append("This is a text audit only; it does not assign or prove security modes.")
    return notes


def build_report() -> dict[str, object]:
    root = repo_root()
    hits = collect_hits(root)
    requirements = collect_requirements(root)
    headings = collect_headings(root)
    rows = collect_parameter_rows(root)
    summary = summarize_modes(hits)
    return {
        "proof_status": PROOF_STATUS,
        "theorem_or_problem_id": PROBLEM_ID,
        "input_parameters": {
            "source_files": SOURCE_FILES,
            "paper_c_file": PAPER_C_FILE,
            "blueprint_file": BLUEPRINT_FILE,
            "canonical_modes": tuple(MODE_PATTERNS),
        },
        "exact_object": {
            "audit_type": "deterministic LaTeX text scan",
            "random_seed": None,
            "mode_patterns": MODE_PATTERNS,
        },
        "result": {
            "mode_summary": summary,
            "blueprint_requirement_lines": [asdict(item) for item in requirements],
            "paper_c_mode_headings": [asdict(item) for item in headings],
            "parameter_rows": [asdict(item) for item in rows],
            "notes": build_notes(summary, rows),
        },
        "proof_certificate": {
            "certificate_kind": "line-numbered grep-style witness list",
            "hits": [asdict(hit) for hit in hits],
        },
    }


def print_text(report: dict[str, object]) -> None:
    result = report["result"]
    summary = result["mode_summary"]
    print("Security mode label audit")
    print(f"Proof status: {report['proof_status']}")
    print(f"Theorem/problem ID: {report['theorem_or_problem_id']}")
    print("Input params:")
    for source in report["input_parameters"]["source_files"]:
        print(f"  source_file={source}")
    print("Exact object: deterministic LaTeX text scan; random_seed=None")
    print("")
    print("Mode summary:")
    for mode, data in summary.items():
        strict = data["strict_hits_in_paper_c"]
        loose = data["loose_hits_in_paper_c"]
        missing = data["strict_missing_in_paper_c"]
        print(f"  {mode}: paper_c_strict={strict}, paper_c_loose={loose}, missing={missing}")
    print("")
    print("Paper C mode/fallback headings:")
    for heading in result["paper_c_mode_headings"]:
        mode = heading["matched_mode"] or "none"
        print(f"  {heading['file']}:{heading['line']}: {heading['heading']} [{mode}]")
    print("")
    print("Parameter table rows:")
    for row in result["parameter_rows"]:
        inline = ", ".join(row["inline_mode_hits"]) or "none"
        hint = row["nearby_caption_hint"] or "none"
        print(f"  {row['file']}:{row['line']}: inline={inline}; hint={hint}")
        print(f"    {row['row']}")
    print("")
    print("Notes:")
    for note in result["notes"]:
        print(f"  - {note}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="output format",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = build_report()
    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_text(report)


if __name__ == "__main__":
    main()
