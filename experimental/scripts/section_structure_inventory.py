#!/usr/bin/env python3
"""Inventory structural headings and labels across stable TeX manuscripts.

Proof status: AUDIT. This deterministic scanner records part, section,
subsection, subsubsection, and paragraph headings, then reports nearby
structural labels, unlabeled numbered headings, and duplicate structural
labels. It does not compile or modify stable TeX.
"""

from __future__ import annotations

import argparse
import bisect
import json
import re
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]

SOURCE_FILES = (
    "tex/RS_disproof_v3.tex",
    "tex/slackMCA_v4.tex",
    "tex/cs25_cap_v12.tex",
    "tex/snarks_v5.tex",
    "tex/proximity_blueprint_v3.tex",
)

THEOREM_PROBLEM_ID = "stable-tex-section-structure-inventory"
PROOF_STATUS = "AUDIT"
DETERMINISM = "deterministic source scan; no random seed"

HEADING_COMMANDS = (
    "subsubsection",
    "subsection",
    "paragraph",
    "section",
    "part",
)
LABEL_RECOMMENDED_LEVELS = {
    "part",
    "section",
    "subsection",
    "subsubsection",
}
LABEL_LOOKAHEAD_LINES = 3

HEADING_RE = re.compile(
    r"\\(?P<command>"
    + "|".join(re.escape(command) for command in HEADING_COMMANDS)
    + r")(?P<star>\*)?(?![A-Za-z])"
)
LABEL_RE = re.compile(r"\\label\{(?P<label>[^{}]+)\}")


@dataclass(frozen=True)
class HeadingEntry:
    file: str
    line: int
    command: str
    starred: bool
    numbered: bool
    title: str
    label: str | None
    label_line: int | None


def strip_tex_comment(line: str) -> str:
    backslashes = 0
    for index, char in enumerate(line):
        if char == "\\":
            backslashes += 1
            continue
        if char == "%" and backslashes % 2 == 0:
            return line[:index]
        backslashes = 0
    return line


def stripped_source(relative_path: str) -> tuple[list[str], str, list[int]]:
    path = REPO_ROOT / relative_path
    lines = [
        strip_tex_comment(line)
        for line in path.read_text(encoding="utf-8").splitlines()
    ]
    text = "\n".join(lines)
    if text:
        text += "\n"

    line_starts = [0]
    for index, char in enumerate(text):
        if char == "\n" and index + 1 < len(text):
            line_starts.append(index + 1)
    return lines, text, line_starts


def line_number_for(index: int, line_starts: list[int]) -> int:
    return bisect.bisect_right(line_starts, index)


def is_escaped(text: str, index: int) -> bool:
    backslashes = 0
    cursor = index - 1
    while cursor >= 0 and text[cursor] == "\\":
        backslashes += 1
        cursor -= 1
    return backslashes % 2 == 1


def skip_whitespace(text: str, index: int) -> int:
    while index < len(text) and text[index].isspace():
        index += 1
    return index


def find_matching(
    text: str,
    open_index: int,
    open_char: str,
    close_char: str,
) -> int | None:
    depth = 0
    for index in range(open_index, len(text)):
        char = text[index]
        if is_escaped(text, index):
            continue
        if char == open_char:
            depth += 1
            continue
        if char == close_char:
            depth -= 1
            if depth == 0:
                return index
    return None


def find_heading_title_span(text: str, index: int) -> tuple[int, int] | None:
    cursor = skip_whitespace(text, index)
    if cursor < len(text) and text[cursor] == "[":
        close_optional = find_matching(text, cursor, "[", "]")
        if close_optional is None:
            return None
        cursor = skip_whitespace(text, close_optional + 1)

    if cursor >= len(text) or text[cursor] != "{":
        return None

    close_title = find_matching(text, cursor, "{", "}")
    if close_title is None:
        return None
    return cursor, close_title


def normalise_title(value: str) -> str:
    return " ".join(value.split())


def nearby_label(
    lines: list[str],
    end_line: int,
    end_column: int,
) -> tuple[str | None, int | None]:
    same_line = lines[end_line - 1][end_column:]
    match = LABEL_RE.search(same_line)
    if match:
        return match.group("label"), end_line

    for offset in range(1, LABEL_LOOKAHEAD_LINES + 1):
        candidate_line = end_line + offset
        if candidate_line > len(lines):
            break

        candidate = lines[candidate_line - 1].strip()
        if not candidate:
            continue

        match = LABEL_RE.match(candidate)
        if match:
            return match.group("label"), candidate_line

        if not candidate.startswith(r"\label"):
            break

    return None, None


def scan_file(relative_path: str) -> list[HeadingEntry]:
    lines, text, line_starts = stripped_source(relative_path)
    entries: list[HeadingEntry] = []

    for match in HEADING_RE.finditer(text):
        span = find_heading_title_span(text, match.end())
        if span is None:
            continue

        title_open, title_close = span
        start_line = line_number_for(match.start(), line_starts)
        end_line = line_number_for(title_close, line_starts)
        end_column = title_close - line_starts[end_line - 1] + 1
        label, label_line = nearby_label(lines, end_line, end_column)
        command = match.group("command")
        starred = bool(match.group("star"))

        entries.append(
            HeadingEntry(
                file=relative_path,
                line=start_line,
                command=command,
                starred=starred,
                numbered=not starred,
                title=normalise_title(text[title_open + 1 : title_close]),
                label=label,
                label_line=label_line,
            )
        )

    return entries


def is_label_recommended(entry: HeadingEntry) -> bool:
    return entry.numbered and entry.command in LABEL_RECOMMENDED_LEVELS


def duplicate_structural_labels(
    entries: list[HeadingEntry],
) -> dict[str, list[HeadingEntry]]:
    by_label: dict[str, list[HeadingEntry]] = defaultdict(list)
    for entry in entries:
        if entry.label:
            by_label[entry.label].append(entry)
    return {
        label: label_entries
        for label, label_entries in sorted(by_label.items())
        if len(label_entries) > 1
    }


def build_report(entries: list[HeadingEntry]) -> dict[str, Any]:
    counts_by_command = Counter(entry.command for entry in entries)
    starred_by_command = Counter(entry.command for entry in entries if entry.starred)
    numbered_by_command = Counter(entry.command for entry in entries if entry.numbered)
    labeled_by_command = Counter(entry.command for entry in entries if entry.label)
    counts_by_file: dict[str, dict[str, int]] = {}

    for source in SOURCE_FILES:
        source_entries = [entry for entry in entries if entry.file == source]
        counts_by_file[source] = {
            "total": len(source_entries),
            "numbered": sum(entry.numbered for entry in source_entries),
            "starred": sum(entry.starred for entry in source_entries),
            "labeled": sum(entry.label is not None for entry in source_entries),
            "unlabeled_recommended": sum(
                is_label_recommended(entry) and entry.label is None
                for entry in source_entries
            ),
        }

    unlabeled_recommended = [
        entry
        for entry in entries
        if is_label_recommended(entry) and entry.label is None
    ]
    duplicates = duplicate_structural_labels(entries)
    audit_result = "PASS"
    if unlabeled_recommended or duplicates:
        audit_result = "REVIEW"

    return {
        "metadata": {
            "proof_status": PROOF_STATUS,
            "theorem_problem_id": THEOREM_PROBLEM_ID,
            "determinism": DETERMINISM,
            "input_files": list(SOURCE_FILES),
            "label_lookahead_lines": LABEL_LOOKAHEAD_LINES,
            "label_recommended_levels": sorted(LABEL_RECOMMENDED_LEVELS),
        },
        "result": {
            "audit_result": audit_result,
            "total_headings": len(entries),
            "numbered_headings": sum(entry.numbered for entry in entries),
            "starred_headings": sum(entry.starred for entry in entries),
            "labeled_headings": sum(entry.label is not None for entry in entries),
            "unlabeled_recommended_headings": len(unlabeled_recommended),
            "duplicate_structural_labels": len(duplicates),
        },
        "counts": {
            "by_command": dict(sorted(counts_by_command.items())),
            "numbered_by_command": dict(sorted(numbered_by_command.items())),
            "starred_by_command": dict(sorted(starred_by_command.items())),
            "labeled_by_command": dict(sorted(labeled_by_command.items())),
            "by_file": counts_by_file,
        },
        "unlabeled_recommended_headings": [
            asdict(entry) for entry in unlabeled_recommended
        ],
        "duplicate_structural_labels": {
            label: [asdict(entry) for entry in label_entries]
            for label, label_entries in duplicates.items()
        },
        "headings": [asdict(entry) for entry in entries],
    }


def format_heading(entry: dict[str, Any]) -> str:
    label = entry["label"] if entry["label"] else "<none>"
    return (
        f"{entry['file']}:{entry['line']} "
        f"\\{entry['command']} label={label} title={entry['title']!r}"
    )


def format_text(report: dict[str, Any]) -> str:
    metadata = report["metadata"]
    result = report["result"]
    counts = report["counts"]
    lines = [
        "Section structure inventory",
        f"Proof status: {metadata['proof_status']}",
        f"Theorem/problem id: {metadata['theorem_problem_id']}",
        f"Determinism: {metadata['determinism']}",
        f"Audit result: {result['audit_result']}",
        "",
        "Summary:",
        f"  total headings: {result['total_headings']}",
        f"  numbered headings: {result['numbered_headings']}",
        f"  starred headings: {result['starred_headings']}",
        f"  labeled headings: {result['labeled_headings']}",
        "  unlabeled recommended headings: "
        f"{result['unlabeled_recommended_headings']}",
        f"  duplicate structural labels: {result['duplicate_structural_labels']}",
        "",
        "By command:",
    ]

    for command, count in counts["by_command"].items():
        numbered = counts["numbered_by_command"].get(command, 0)
        starred = counts["starred_by_command"].get(command, 0)
        labeled = counts["labeled_by_command"].get(command, 0)
        lines.append(
            f"  - {command}: {count} total, {numbered} numbered, "
            f"{starred} starred, {labeled} labeled"
        )

    lines.append("")
    lines.append("By file:")
    for source, source_counts in counts["by_file"].items():
        lines.append(
            f"  - {source}: {source_counts['total']} total, "
            f"{source_counts['labeled']} labeled, "
            f"{source_counts['unlabeled_recommended']} unlabeled recommended"
        )

    lines.append("")
    lines.append("Unlabeled recommended headings:")
    unlabeled = report["unlabeled_recommended_headings"]
    if unlabeled:
        for entry in unlabeled:
            lines.append(f"  - {format_heading(entry)}")
    else:
        lines.append("  - none")

    lines.append("")
    lines.append("Duplicate structural labels:")
    duplicates = report["duplicate_structural_labels"]
    if duplicates:
        for label, entries in duplicates.items():
            locations = ", ".join(
                f"{entry['file']}:{entry['line']}" for entry in entries
            )
            lines.append(f"  - {label}: {locations}")
    else:
        lines.append("  - none")

    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Inventory structural TeX headings and nearby labels across the "
            "stable manuscripts."
        )
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    entries: list[HeadingEntry] = []
    for source in SOURCE_FILES:
        entries.extend(scan_file(source))

    report = build_report(entries)
    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(format_text(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
