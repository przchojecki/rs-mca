#!/usr/bin/env python3
"""Inventory manuscript topmatter metadata across stable TeX sources.

Proof status: AUDIT. This deterministic scanner records title, author, date,
maketitle, and abstract spans for each stable manuscript. It flags missing or
duplicate topmatter fields, ordering issues, and dynamic dates such as
``\\today`` that can affect release reproducibility.
"""

from __future__ import annotations

import argparse
import bisect
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]

SOURCE_FILES = (
    "tex/RS_disproof_v3.tex",
    "tex/slackMCA_v3.tex",
    "tex/cs25_cap_v4.tex",
    "tex/snarks_v4.tex",
    "tex/proximity_blueprint_v3.tex",
)

THEOREM_PROBLEM_ID = "stable-tex-topmatter-metadata-inventory"
PROOF_STATUS = "AUDIT"
DETERMINISM = "deterministic source scan; no random seed"

METADATA_COMMANDS = ("title", "author", "date")
METADATA_RE = re.compile(r"\\(?P<command>title|author|date)(?![A-Za-z])\s*\{")
MAKETITLE_RE = re.compile(r"\\maketitle(?![A-Za-z])")
ABSTRACT_BEGIN_RE = re.compile(r"\\begin\{abstract\}")
ABSTRACT_END_RE = re.compile(r"\\end\{abstract\}")
WORD_RE = re.compile(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?")


@dataclass(frozen=True)
class MetadataEntry:
    file: str
    command: str
    line: int
    value: str
    is_dynamic_date: bool


@dataclass(frozen=True)
class MaketitleEntry:
    file: str
    line: int


@dataclass(frozen=True)
class AbstractEntry:
    file: str
    begin_line: int
    end_line: int | None
    word_count: int
    text_preview: str


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


def find_matching_brace(text: str, open_index: int) -> int | None:
    depth = 0
    for index in range(open_index, len(text)):
        char = text[index]
        if is_escaped(text, index):
            continue
        if char == "{":
            depth += 1
            continue
        if char == "}":
            depth -= 1
            if depth == 0:
                return index
    return None


def normalise_text(value: str) -> str:
    return " ".join(value.split())


def word_count(value: str) -> int:
    return len(WORD_RE.findall(value))


def preview(value: str, limit: int = 120) -> str:
    normalised = normalise_text(value)
    if len(normalised) <= limit:
        return normalised
    return normalised[: limit - 3].rstrip() + "..."


def scan_metadata_commands(
    relative_path: str,
    text: str,
    line_starts: list[int],
) -> list[MetadataEntry]:
    entries: list[MetadataEntry] = []
    for match in METADATA_RE.finditer(text):
        open_brace = match.end() - 1
        close_brace = find_matching_brace(text, open_brace)
        if close_brace is None:
            continue

        command = match.group("command")
        value = normalise_text(text[open_brace + 1 : close_brace])
        entries.append(
            MetadataEntry(
                file=relative_path,
                command=command,
                line=line_number_for(match.start(), line_starts),
                value=value,
                is_dynamic_date=command == "date" and r"\today" in value,
            )
        )
    return entries


def scan_maketitles(
    relative_path: str,
    text: str,
    line_starts: list[int],
) -> list[MaketitleEntry]:
    return [
        MaketitleEntry(
            file=relative_path,
            line=line_number_for(match.start(), line_starts),
        )
        for match in MAKETITLE_RE.finditer(text)
    ]


def scan_abstracts(
    relative_path: str,
    text: str,
    line_starts: list[int],
) -> list[AbstractEntry]:
    entries: list[AbstractEntry] = []
    search_from = 0
    while True:
        begin_match = ABSTRACT_BEGIN_RE.search(text, search_from)
        if begin_match is None:
            break

        end_match = ABSTRACT_END_RE.search(text, begin_match.end())
        if end_match is None:
            body = text[begin_match.end() :]
            end_line = None
            search_from = len(text)
        else:
            body = text[begin_match.end() : end_match.start()]
            end_line = line_number_for(end_match.start(), line_starts)
            search_from = end_match.end()

        entries.append(
            AbstractEntry(
                file=relative_path,
                begin_line=line_number_for(begin_match.start(), line_starts),
                end_line=end_line,
                word_count=word_count(body),
                text_preview=preview(body),
            )
        )
    return entries


def scan_file(
    relative_path: str,
) -> tuple[list[MetadataEntry], list[MaketitleEntry], list[AbstractEntry]]:
    _lines, text, line_starts = stripped_source(relative_path)
    return (
        scan_metadata_commands(relative_path, text, line_starts),
        scan_maketitles(relative_path, text, line_starts),
        scan_abstracts(relative_path, text, line_starts),
    )


def entries_by_command(entries: list[MetadataEntry]) -> dict[str, list[MetadataEntry]]:
    return {
        command: [entry for entry in entries if entry.command == command]
        for command in METADATA_COMMANDS
    }


def ordering_issues(
    entries: list[MetadataEntry],
    maketitles: list[MaketitleEntry],
    abstracts: list[AbstractEntry],
) -> list[str]:
    issues: list[str] = []
    if not maketitles:
        return issues

    first_maketitle_line = min(entry.line for entry in maketitles)
    for command_entries in entries_by_command(entries).values():
        for entry in command_entries:
            if entry.line > first_maketitle_line:
                issues.append(
                    f"\\{entry.command} at line {entry.line} appears after "
                    f"\\maketitle at line {first_maketitle_line}"
                )

    for abstract in abstracts:
        if abstract.begin_line < first_maketitle_line:
            issues.append(
                f"abstract at line {abstract.begin_line} appears before "
                f"\\maketitle at line {first_maketitle_line}"
            )
    return issues


def build_file_report(
    source: str,
    entries: list[MetadataEntry],
    maketitles: list[MaketitleEntry],
    abstracts: list[AbstractEntry],
) -> dict[str, Any]:
    command_entries = entries_by_command(entries)
    missing_fields = [
        command for command, values in command_entries.items() if not values
    ]
    duplicate_fields = {
        command: [asdict(entry) for entry in values]
        for command, values in command_entries.items()
        if len(values) > 1
    }
    dynamic_dates = [
        asdict(entry) for entry in command_entries["date"] if entry.is_dynamic_date
    ]
    unclosed_abstracts = [
        asdict(entry) for entry in abstracts if entry.end_line is None
    ]
    file_ordering_issues = ordering_issues(entries, maketitles, abstracts)
    review_items = []
    if missing_fields:
        review_items.append("missing topmatter fields")
    if duplicate_fields:
        review_items.append("duplicate topmatter fields")
    if len(maketitles) != 1:
        review_items.append("maketitle count is not one")
    if len(abstracts) != 1:
        review_items.append("abstract count is not one")
    if dynamic_dates:
        review_items.append("dynamic date")
    if unclosed_abstracts:
        review_items.append("unclosed abstract")
    if file_ordering_issues:
        review_items.append("topmatter ordering")

    return {
        "file": source,
        "audit_result": "REVIEW" if review_items else "PASS",
        "review_items": review_items,
        "missing_fields": missing_fields,
        "duplicate_fields": duplicate_fields,
        "dynamic_dates": dynamic_dates,
        "ordering_issues": file_ordering_issues,
        "metadata": {
            command: [asdict(entry) for entry in values]
            for command, values in command_entries.items()
        },
        "maketitles": [asdict(entry) for entry in maketitles],
        "abstracts": [asdict(entry) for entry in abstracts],
    }


def build_report() -> dict[str, Any]:
    file_reports = []
    all_entries: list[MetadataEntry] = []
    all_maketitles: list[MaketitleEntry] = []
    all_abstracts: list[AbstractEntry] = []

    for source in SOURCE_FILES:
        entries, maketitles, abstracts = scan_file(source)
        all_entries.extend(entries)
        all_maketitles.extend(maketitles)
        all_abstracts.extend(abstracts)
        file_reports.append(
            build_file_report(source, entries, maketitles, abstracts)
        )

    dynamic_date_count = sum(
        len(file_report["dynamic_dates"]) for file_report in file_reports
    )
    review_files = [
        file_report["file"]
        for file_report in file_reports
        if file_report["audit_result"] == "REVIEW"
    ]

    return {
        "metadata": {
            "proof_status": PROOF_STATUS,
            "theorem_problem_id": THEOREM_PROBLEM_ID,
            "determinism": DETERMINISM,
            "input_files": list(SOURCE_FILES),
        },
        "result": {
            "audit_result": "REVIEW" if review_files else "PASS",
            "files_scanned": len(SOURCE_FILES),
            "review_files": len(review_files),
            "metadata_commands": len(all_entries),
            "maketitle_commands": len(all_maketitles),
            "abstract_environments": len(all_abstracts),
            "dynamic_dates": dynamic_date_count,
        },
        "files": file_reports,
    }


def format_file_summary(file_report: dict[str, Any]) -> str:
    title_entries = file_report["metadata"]["title"]
    author_entries = file_report["metadata"]["author"]
    date_entries = file_report["metadata"]["date"]
    abstract_entries = file_report["abstracts"]
    title = title_entries[0]["value"] if title_entries else "<missing>"
    author = author_entries[0]["value"] if author_entries else "<missing>"
    date = date_entries[0]["value"] if date_entries else "<missing>"
    abstract_words = (
        abstract_entries[0]["word_count"] if abstract_entries else "<missing>"
    )
    return (
        f"  - {file_report['file']}: {file_report['audit_result']}; "
        f"title={title!r}; author={author!r}; date={date!r}; "
        f"abstract_words={abstract_words}"
    )


def format_text(report: dict[str, Any]) -> str:
    metadata = report["metadata"]
    result = report["result"]
    lines = [
        "Topmatter metadata inventory",
        f"Proof status: {metadata['proof_status']}",
        f"Theorem/problem id: {metadata['theorem_problem_id']}",
        f"Determinism: {metadata['determinism']}",
        f"Audit result: {result['audit_result']}",
        "",
        "Summary:",
        f"  files scanned: {result['files_scanned']}",
        f"  review files: {result['review_files']}",
        f"  metadata commands: {result['metadata_commands']}",
        f"  maketitle commands: {result['maketitle_commands']}",
        f"  abstract environments: {result['abstract_environments']}",
        f"  dynamic dates: {result['dynamic_dates']}",
        "",
        "Per-file metadata:",
    ]

    for file_report in report["files"]:
        lines.append(format_file_summary(file_report))

    lines.append("")
    lines.append("Review items:")
    review_lines = []
    for file_report in report["files"]:
        if not file_report["review_items"]:
            continue
        items = ", ".join(file_report["review_items"])
        review_lines.append(f"  - {file_report['file']}: {items}")

    if review_lines:
        lines.extend(review_lines)
    else:
        lines.append("  - none")

    lines.append("")
    lines.append("Dynamic dates:")
    dynamic_dates = [
        (file_report["file"], entry)
        for file_report in report["files"]
        for entry in file_report["dynamic_dates"]
    ]
    if dynamic_dates:
        for source, entry in dynamic_dates:
            lines.append(f"  - {source}:{entry['line']} date={entry['value']!r}")
    else:
        lines.append("  - none")

    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Inventory stable TeX topmatter metadata and release-hygiene "
            "signals."
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
    report = build_report()
    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(format_text(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
