#!/usr/bin/env python3
"""Audit TeX label/reference integrity in the stable manuscripts.

Proof status: AUDIT.

The manuscripts are standalone TeX files, so this audit checks references within
each file rather than assuming all labels share one global namespace.  It
reports line-numbered labels, references, undefined same-file references,
within-file duplicate labels, and unused labels.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path


TEX_FILES = (
    "tex/RS_disproof_v3.tex",
    "tex/slackMCA_v3.tex",
    "tex/cs25_cap_v4.tex",
    "tex/snarks_v4.tex",
    "tex/proximity_blueprint_v3.tex",
)
REFERENCE_COMMANDS = ("cref", "Cref", "eqref", "ref", "autoref", "pageref")
PROOF_STATUS = "AUDIT"
PROBLEM_ID = "Stable-TeX reference integrity audit"


LABEL_RE = re.compile(r"\\label\{(?P<label>[^}]+)\}")
REF_RE = re.compile(
    r"\\(?P<command>"
    + "|".join(re.escape(command) for command in REFERENCE_COMMANDS)
    + r")\s*\{(?P<labels>[^}]+)\}"
)


@dataclass(frozen=True)
class LabelOccurrence:
    file: str
    line: int
    label: str
    snippet: str


@dataclass(frozen=True)
class ReferenceOccurrence:
    file: str
    line: int
    command: str
    label: str
    raw_argument: str
    snippet: str


@dataclass(frozen=True)
class UndefinedReference:
    file: str
    line: int
    command: str
    label: str
    raw_argument: str
    snippet: str


@dataclass(frozen=True)
class DuplicateLabel:
    file: str
    label: str
    lines: tuple[int, ...]


@dataclass(frozen=True)
class CrossFileDuplicateLabel:
    label: str
    locations: tuple[str, ...]


@dataclass(frozen=True)
class UnusedLabel:
    file: str
    line: int
    label: str
    snippet: str


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def clean_snippet(line: str) -> str:
    return re.sub(r"\s+", " ", line.strip())


def strip_comment(line: str) -> str:
    escaped = False
    for index, char in enumerate(line):
        if char == "\\" and not escaped:
            escaped = True
            continue
        if char == "%" and not escaped:
            return line[:index]
        escaped = False
    return line


def split_reference_argument(argument: str) -> list[str]:
    return [item.strip() for item in argument.split(",") if item.strip()]


def read_lines(root: Path, relative_path: str) -> list[str]:
    return (root / relative_path).read_text(encoding="utf-8").splitlines()


def scan_file(
    root: Path,
    relative_path: str,
) -> tuple[list[LabelOccurrence], list[ReferenceOccurrence]]:
    labels: list[LabelOccurrence] = []
    references: list[ReferenceOccurrence] = []
    for line_no, raw_line in enumerate(read_lines(root, relative_path), start=1):
        line = strip_comment(raw_line)
        snippet = clean_snippet(line)
        for match in LABEL_RE.finditer(line):
            labels.append(
                LabelOccurrence(
                    file=relative_path,
                    line=line_no,
                    label=match.group("label").strip(),
                    snippet=snippet,
                )
            )
        for match in REF_RE.finditer(line):
            command = match.group("command")
            raw_argument = match.group("labels")
            for label in split_reference_argument(raw_argument):
                references.append(
                    ReferenceOccurrence(
                        file=relative_path,
                        line=line_no,
                        command=command,
                        label=label,
                        raw_argument=raw_argument,
                        snippet=snippet,
                    )
                )
    return labels, references


def collect_occurrences() -> tuple[list[LabelOccurrence], list[ReferenceOccurrence]]:
    root = repo_root()
    labels: list[LabelOccurrence] = []
    references: list[ReferenceOccurrence] = []
    for relative_path in TEX_FILES:
        file_labels, file_references = scan_file(root, relative_path)
        labels.extend(file_labels)
        references.extend(file_references)
    return labels, references


def labels_by_file(labels: list[LabelOccurrence]) -> dict[str, set[str]]:
    grouped = {file_name: set() for file_name in TEX_FILES}
    for label in labels:
        grouped.setdefault(label.file, set()).add(label.label)
    return grouped


def references_by_file(references: list[ReferenceOccurrence]) -> dict[str, set[str]]:
    grouped = {file_name: set() for file_name in TEX_FILES}
    for reference in references:
        grouped.setdefault(reference.file, set()).add(reference.label)
    return grouped


def undefined_references(
    labels: list[LabelOccurrence],
    references: list[ReferenceOccurrence],
) -> list[UndefinedReference]:
    label_sets = labels_by_file(labels)
    missing: list[UndefinedReference] = []
    for reference in references:
        if reference.label in label_sets.get(reference.file, set()):
            continue
        missing.append(
            UndefinedReference(
                file=reference.file,
                line=reference.line,
                command=reference.command,
                label=reference.label,
                raw_argument=reference.raw_argument,
                snippet=reference.snippet,
            )
        )
    return missing


def duplicate_labels_by_file(labels: list[LabelOccurrence]) -> list[DuplicateLabel]:
    grouped: dict[tuple[str, str], list[int]] = {}
    for label in labels:
        grouped.setdefault((label.file, label.label), []).append(label.line)
    duplicates = [
        DuplicateLabel(file=file_name, label=label, lines=tuple(lines))
        for (file_name, label), lines in sorted(grouped.items())
        if len(lines) > 1
    ]
    return duplicates


def duplicate_labels_cross_file(labels: list[LabelOccurrence]) -> list[CrossFileDuplicateLabel]:
    grouped: dict[str, list[str]] = {}
    for label in labels:
        location = f"{label.file}:{label.line}"
        grouped.setdefault(label.label, []).append(location)
    duplicates = [
        CrossFileDuplicateLabel(label=label, locations=tuple(locations))
        for label, locations in sorted(grouped.items())
        if len({location.split(":", 1)[0] for location in locations}) > 1
    ]
    return duplicates


def unused_labels(
    labels: list[LabelOccurrence],
    references: list[ReferenceOccurrence],
) -> list[UnusedLabel]:
    reference_sets = references_by_file(references)
    unused: list[UnusedLabel] = []
    for label in labels:
        if label.label in reference_sets.get(label.file, set()):
            continue
        unused.append(
            UnusedLabel(
                file=label.file,
                line=label.line,
                label=label.label,
                snippet=label.snippet,
            )
        )
    return unused


def count_by_file(
    labels: list[LabelOccurrence],
    references: list[ReferenceOccurrence],
    missing: list[UndefinedReference],
    duplicates: list[DuplicateLabel],
    unused: list[UnusedLabel],
) -> dict[str, dict[str, int]]:
    counts: dict[str, dict[str, int]] = {
        file_name: {
            "labels": 0,
            "references": 0,
            "undefined_references": 0,
            "within_file_duplicate_labels": 0,
            "unused_labels": 0,
        }
        for file_name in TEX_FILES
    }
    for label in labels:
        counts[label.file]["labels"] += 1
    for reference in references:
        counts[reference.file]["references"] += 1
    for item in missing:
        counts[item.file]["undefined_references"] += 1
    for item in duplicates:
        counts[item.file]["within_file_duplicate_labels"] += 1
    for item in unused:
        counts[item.file]["unused_labels"] += 1
    return counts


def count_reference_commands(references: list[ReferenceOccurrence]) -> dict[str, int]:
    counts: dict[str, int] = {command: 0 for command in REFERENCE_COMMANDS}
    for reference in references:
        counts[reference.command] = counts.get(reference.command, 0) + 1
    return {command: count for command, count in counts.items() if count}


def build_notes(
    missing: list[UndefinedReference],
    duplicates: list[DuplicateLabel],
    cross_file_duplicates: list[CrossFileDuplicateLabel],
    unused: list[UnusedLabel],
) -> list[str]:
    notes: list[str] = []
    if missing:
        notes.append(f"{len(missing)} same-file references point to undefined labels.")
    if duplicates:
        notes.append(f"{len(duplicates)} labels are duplicated within a manuscript.")
    if cross_file_duplicates:
        notes.append(
            f"{len(cross_file_duplicates)} labels occur in more than one manuscript; "
            "this is informational because the TeX files are standalone."
        )
    if unused:
        notes.append(
            f"{len(unused)} labels are not referenced within their own manuscript."
        )
    notes.append("This is a syntactic audit only; it does not run LaTeX.")
    return notes


def build_report() -> dict[str, object]:
    labels, references = collect_occurrences()
    missing = undefined_references(labels, references)
    duplicates = duplicate_labels_by_file(labels)
    cross_file_duplicates = duplicate_labels_cross_file(labels)
    unused = unused_labels(labels, references)
    return {
        "proof_status": PROOF_STATUS,
        "theorem_or_problem_id": PROBLEM_ID,
        "input_parameters": {
            "source_files": TEX_FILES,
            "reference_commands": REFERENCE_COMMANDS,
        },
        "exact_object": {
            "audit_type": "line-based same-file TeX label/reference scan",
            "label_pattern": LABEL_RE.pattern,
            "reference_pattern": REF_RE.pattern,
            "random_seed": None,
        },
        "result": {
            "total_labels": len(labels),
            "total_references": len(references),
            "undefined_reference_count": len(missing),
            "within_file_duplicate_label_count": len(duplicates),
            "cross_file_duplicate_label_count": len(cross_file_duplicates),
            "unused_label_count": len(unused),
            "reference_command_counts": count_reference_commands(references),
            "counts_by_file": count_by_file(labels, references, missing, duplicates, unused),
            "notes": build_notes(missing, duplicates, cross_file_duplicates, unused),
        },
        "proof_certificate": {
            "label_occurrences": [asdict(item) for item in labels],
            "reference_occurrences": [asdict(item) for item in references],
            "undefined_references": [asdict(item) for item in missing],
            "within_file_duplicate_labels": [asdict(item) for item in duplicates],
            "cross_file_duplicate_labels": [asdict(item) for item in cross_file_duplicates],
            "unused_labels": [asdict(item) for item in unused],
        },
    }


def print_issue_list(title: str, items: list[dict[str, object]], limit: int = 20) -> None:
    print("")
    print(title + ":")
    if not items:
        print("  none")
        return
    for item in items[:limit]:
        if "command" in item:
            print(
                f"  {item['file']}:{item['line']}: "
                f"\\{item['command']}{{{item['raw_argument']}}} -> {item['label']}"
            )
        elif "lines" in item:
            lines = ", ".join(str(line) for line in item["lines"])
            print(f"  {item['file']}: {item['label']} at lines {lines}")
        elif "locations" in item:
            locations = ", ".join(item["locations"])
            print(f"  {item['label']}: {locations}")
        else:
            print(f"  {item['file']}:{item['line']}: {item['label']}")
    if len(items) > limit:
        print(f"  ... {len(items) - limit} more; use --format json for full output")


def print_text(report: dict[str, object]) -> None:
    result = report["result"]
    certificate = report["proof_certificate"]
    print("TeX reference integrity audit")
    print(f"Proof status: {report['proof_status']}")
    print(f"Theorem/problem ID: {report['theorem_or_problem_id']}")
    print("Input params:")
    for source in report["input_parameters"]["source_files"]:
        print(f"  source_file={source}")
    print("Exact object: line-based same-file TeX label/reference scan; random_seed=None")
    print("")
    print("Summary:")
    print(f"  total_labels={result['total_labels']}")
    print(f"  total_references={result['total_references']}")
    print(f"  undefined_references={result['undefined_reference_count']}")
    print(f"  within_file_duplicate_labels={result['within_file_duplicate_label_count']}")
    print(f"  cross_file_duplicate_labels={result['cross_file_duplicate_label_count']}")
    print(f"  unused_labels={result['unused_label_count']}")
    print("")
    print("Counts by file:")
    for file_name, counts in result["counts_by_file"].items():
        rendered = ", ".join(f"{name}={count}" for name, count in counts.items())
        print(f"  {file_name}: {rendered}")
    print_issue_list("Undefined same-file references", certificate["undefined_references"])
    print_issue_list("Within-file duplicate labels", certificate["within_file_duplicate_labels"])
    print_issue_list("Cross-file duplicate labels", certificate["cross_file_duplicate_labels"])
    print_issue_list("Unused labels", certificate["unused_labels"])
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
