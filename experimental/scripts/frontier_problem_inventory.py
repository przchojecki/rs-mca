#!/usr/bin/env python3
"""Inventory frontier environments in the stable TeX manuscripts.

Proof status: AUDIT.

This is a deterministic coordination aid for agents.  It extracts problem,
openproblem, conjecture, assumption, and designrule blocks from the stable TeX
sources, records their line ranges and labels, and flags unlabeled or duplicate
frontier blocks.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path


TEX_FILES = (
    "tex/RS_disproof_v3.tex",
    "tex/slackMCA_v4.tex",
    "tex/cs25_cap_v12.tex",
    "tex/snarks_v5.tex",
    "tex/proximity_blueprint_v3.tex",
)
ENVIRONMENTS = ("problem", "openproblem", "conjecture", "assumption", "designrule")
PROOF_STATUS = "AUDIT"
PROBLEM_ID = "Agent guide frontier inventory / manuscript open-problem surface"


BEGIN_RE = re.compile(
    r"\\begin\{(?P<env>"
    + "|".join(re.escape(name) for name in ENVIRONMENTS)
    + r")\}(?:\[(?P<title>[^\]]*)\])?"
)
LABEL_RE = re.compile(r"\\label\{(?P<label>[^}]+)\}")
SECTION_RE = re.compile(r"\\(?P<level>section|subsection|subsubsection)\{(?P<title>[^}]*)\}")
FRONTIER_ID_RE = re.compile(r"^(?P<id>[A-Z][0-9]+)\b")


@dataclass(frozen=True)
class FrontierEntry:
    file: str
    start_line: int
    end_line: int
    environment: str
    title: str | None
    label: str | None
    section: str | None
    frontier_id: str | None
    status_hint: str
    preview: str


@dataclass(frozen=True)
class DuplicateLabel:
    label: str
    occurrences: tuple[str, ...]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_lines(root: Path, relative_path: str) -> list[str]:
    return (root / relative_path).read_text(encoding="utf-8").splitlines()


def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def extract_preview(block_lines: list[str]) -> str:
    body_lines = []
    for line in block_lines:
        stripped = clean_text(line)
        if not stripped:
            continue
        if stripped.startswith(r"\begin{") or stripped.startswith(r"\end{"):
            continue
        stripped = LABEL_RE.sub("", stripped)
        stripped = clean_text(stripped)
        if stripped:
            body_lines.append(stripped)
    preview = clean_text(" ".join(body_lines))
    if len(preview) > 260:
        return preview[:257].rstrip() + "..."
    return preview


def status_hint(environment: str) -> str:
    if environment == "conjecture":
        return "CONJECTURAL"
    if environment == "assumption":
        return "CONDITIONAL_INPUT"
    if environment == "designrule":
        return "DESIGN_RULE"
    return "OPEN_FRONTIER"


def infer_frontier_id(title: str | None, label: str | None) -> str | None:
    candidates = []
    if title:
        candidates.append(title)
    if label:
        candidates.extend(part for part in re.split(r"[:/_-]", label) if part)
    for candidate in candidates:
        match = FRONTIER_ID_RE.search(candidate.strip())
        if match:
            return match.group("id")
    return None


def current_section(line: str, previous: str | None) -> str | None:
    match = SECTION_RE.search(line)
    if match:
        return clean_text(match.group("title"))
    return previous


def find_end_line(lines: list[str], start_index: int, environment: str) -> int:
    end_marker = rf"\end{{{environment}}}"
    for index in range(start_index, len(lines)):
        if end_marker in lines[index]:
            return index
    return len(lines) - 1


def scan_file(root: Path, relative_path: str) -> list[FrontierEntry]:
    lines = read_lines(root, relative_path)
    entries: list[FrontierEntry] = []
    section: str | None = None
    index = 0
    while index < len(lines):
        section = current_section(lines[index], section)
        begin_match = BEGIN_RE.search(lines[index])
        if not begin_match:
            index += 1
            continue

        environment = begin_match.group("env")
        title = begin_match.group("title")
        end_index = find_end_line(lines, index, environment)
        block_lines = lines[index : end_index + 1]
        labels = [match.group("label") for line in block_lines for match in LABEL_RE.finditer(line)]
        label = labels[0] if labels else None
        title = clean_text(title) if title else None
        entries.append(
            FrontierEntry(
                file=relative_path,
                start_line=index + 1,
                end_line=end_index + 1,
                environment=environment,
                title=title,
                label=label,
                section=section,
                frontier_id=infer_frontier_id(title, label),
                status_hint=status_hint(environment),
                preview=extract_preview(block_lines),
            )
        )
        index = end_index + 1
    return entries


def collect_entries() -> list[FrontierEntry]:
    root = repo_root()
    entries: list[FrontierEntry] = []
    for relative_path in TEX_FILES:
        entries.extend(scan_file(root, relative_path))
    return entries


def count_by(entries: list[FrontierEntry], attribute: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for entry in entries:
        key = str(getattr(entry, attribute))
        counts[key] = counts.get(key, 0) + 1
    return dict(sorted(counts.items()))


def count_by_file_and_env(entries: list[FrontierEntry]) -> dict[str, dict[str, int]]:
    counts: dict[str, dict[str, int]] = {}
    for entry in entries:
        file_counts = counts.setdefault(entry.file, {})
        file_counts[entry.environment] = file_counts.get(entry.environment, 0) + 1
    return {
        file_name: dict(sorted(file_counts.items()))
        for file_name, file_counts in sorted(counts.items())
    }


def duplicate_labels(entries: list[FrontierEntry]) -> list[DuplicateLabel]:
    locations: dict[str, list[str]] = {}
    for entry in entries:
        if entry.label is None:
            continue
        locations.setdefault(entry.label, []).append(
            f"{entry.file}:{entry.start_line}-{entry.end_line}"
        )
    duplicates = [
        DuplicateLabel(label=label, occurrences=tuple(occurrences))
        for label, occurrences in sorted(locations.items())
        if len(occurrences) > 1
    ]
    return duplicates


def build_notes(entries: list[FrontierEntry], duplicates: list[DuplicateLabel]) -> list[str]:
    notes: list[str] = []
    missing = [entry for entry in entries if entry.label is None]
    if missing:
        notes.append(
            f"{len(missing)} frontier environments lack labels and cannot be cited stably."
        )
    if duplicates:
        notes.append(f"{len(duplicates)} duplicate labels were found.")
    notes.append(
        "This audit inventories frontier blocks only; it does not prove or rank them."
    )
    return notes


def build_report() -> dict[str, object]:
    entries = collect_entries()
    duplicates = duplicate_labels(entries)
    missing_labels = [entry for entry in entries if entry.label is None]
    return {
        "proof_status": PROOF_STATUS,
        "theorem_or_problem_id": PROBLEM_ID,
        "input_parameters": {
            "source_files": TEX_FILES,
            "environments": ENVIRONMENTS,
        },
        "exact_object": {
            "audit_type": "line-based LaTeX environment inventory",
            "begin_pattern": BEGIN_RE.pattern,
            "label_pattern": LABEL_RE.pattern,
            "random_seed": None,
        },
        "result": {
            "total_entries": len(entries),
            "counts_by_environment": count_by(entries, "environment"),
            "counts_by_status_hint": count_by(entries, "status_hint"),
            "counts_by_file_and_environment": count_by_file_and_env(entries),
            "missing_label_count": len(missing_labels),
            "duplicate_label_count": len(duplicates),
            "notes": build_notes(entries, duplicates),
        },
        "proof_certificate": {
            "entries": [asdict(entry) for entry in entries],
            "missing_labels": [asdict(entry) for entry in missing_labels],
            "duplicate_labels": [asdict(item) for item in duplicates],
        },
    }


def print_counts(report: dict[str, object]) -> None:
    result = report["result"]
    print("Counts by environment:")
    for name, count in result["counts_by_environment"].items():
        print(f"  {name}: {count}")
    print("")
    print("Counts by file:")
    for file_name, counts in result["counts_by_file_and_environment"].items():
        rendered = ", ".join(f"{name}={count}" for name, count in counts.items())
        print(f"  {file_name}: {rendered}")


def print_missing(report: dict[str, object]) -> None:
    missing = report["proof_certificate"]["missing_labels"]
    print("")
    print("Unlabeled frontier environments:")
    if not missing:
        print("  none")
        return
    for entry in missing:
        title = entry["title"] or "(untitled)"
        print(
            f"  {entry['file']}:{entry['start_line']}-{entry['end_line']} "
            f"{entry['environment']} {title}"
        )


def print_duplicates(report: dict[str, object]) -> None:
    duplicates = report["proof_certificate"]["duplicate_labels"]
    print("")
    print("Duplicate labels:")
    if not duplicates:
        print("  none")
        return
    for item in duplicates:
        joined = ", ".join(item["occurrences"])
        print(f"  {item['label']}: {joined}")


def print_entries(report: dict[str, object]) -> None:
    entries = report["proof_certificate"]["entries"]
    print("")
    print("Entries:")
    for entry in entries:
        title = entry["title"] or "(untitled)"
        label = entry["label"] or "NO_LABEL"
        frontier_id = entry["frontier_id"] or "-"
        print(
            f"  {entry['file']}:{entry['start_line']}-{entry['end_line']} "
            f"{entry['environment']} [{label}] {frontier_id}: {title}"
        )


def print_text(report: dict[str, object]) -> None:
    result = report["result"]
    print("Frontier problem inventory")
    print(f"Proof status: {report['proof_status']}")
    print(f"Theorem/problem ID: {report['theorem_or_problem_id']}")
    print("Input params:")
    for source in report["input_parameters"]["source_files"]:
        print(f"  source_file={source}")
    print("Exact object: line-based LaTeX environment inventory; random_seed=None")
    print(f"Total entries: {result['total_entries']}")
    print_counts(report)
    print_missing(report)
    print_duplicates(report)
    print_entries(report)
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
