#!/usr/bin/env python3
"""Inventory theorem-like environments in the stable TeX manuscripts.

Proof status: AUDIT. This is a deterministic scanner, not a mathematical proof.
It reports the exact sources and environment names checked so that later agents
can review result/proof coverage without editing stable TeX.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
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

ENVIRONMENTS = (
    "theorem",
    "lemma",
    "proposition",
    "corollary",
    "definition",
    "remark",
    "example",
    "fact",
    "task",
    "milestone",
)

EXCLUDED_FRONTIER_ENVIRONMENTS = (
    "problem",
    "openproblem",
    "conjecture",
    "assumption",
    "designrule",
)

THEOREM_PROBLEM_ID = "stable-tex-result-environment-inventory"
PROOF_STATUS = "AUDIT"
DETERMINISM = "deterministic; no random seed"

ENV_PATTERN = "|".join(re.escape(env) for env in ENVIRONMENTS)
BEGIN_RE = re.compile(
    rf"\\begin\{{(?P<env>{ENV_PATTERN})\}}"
)
BEGIN_COMMAND_RE = re.compile(r"\\begin\{[^{}]+\}")
END_ANY_RE = re.compile(r"\\end\{[^{}]+\}")
LABEL_RE = re.compile(r"\\label\{(?P<label>[^{}]+)\}")
SECTION_RE = re.compile(
    r"\\(?P<kind>section|subsection|subsubsection)\*?(?:\[[^\]]*\])?\{"
)


@dataclass(frozen=True)
class ResultEntry:
    file: str
    start_line: int
    end_line: int
    environment: str
    title: str | None
    label: str | None
    section: str | None
    preview: str


def strip_tex_comment(line: str) -> str:
    """Remove unescaped TeX comments from a single line."""
    backslashes = 0
    for index, char in enumerate(line):
        if char == "\\":
            backslashes += 1
            continue
        if char == "%" and backslashes % 2 == 0:
            return line[:index]
        backslashes = 0
    return line


def normalise_whitespace(value: str | None) -> str | None:
    if value is None:
        return None
    return " ".join(value.split())


def extract_braced_argument(text: str, opening_brace_index: int) -> str | None:
    depth = 0
    start = opening_brace_index + 1
    for index in range(opening_brace_index, len(text)):
        char = text[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[start:index]
    return None


def extract_optional_argument(text: str, start_index: int) -> tuple[str | None, int]:
    index = start_index
    while index < len(text) and text[index].isspace():
        index += 1
    if index >= len(text) or text[index] != "[":
        return None, start_index

    depth = 0
    for cursor in range(index, len(text)):
        char = text[cursor]
        if char == "[":
            depth += 1
        elif char == "]":
            depth -= 1
            if depth == 0:
                return text[index + 1 : cursor], cursor + 1
    return None, start_index


def remove_begin_commands(line: str) -> str:
    pieces: list[str] = []
    cursor = 0
    for match in BEGIN_COMMAND_RE.finditer(line):
        pieces.append(line[cursor : match.start()])
        _title, cursor = extract_optional_argument(line, match.end())
    pieces.append(line[cursor:])
    return "".join(pieces)


def update_section_context(
    line: str, section_stack: dict[str, str | None]
) -> None:
    for match in SECTION_RE.finditer(line):
        title = extract_braced_argument(line, match.end() - 1)
        title = normalise_whitespace(title)
        if not title:
            continue
        kind = match.group("kind")
        if kind == "section":
            section_stack["section"] = title
            section_stack["subsection"] = None
            section_stack["subsubsection"] = None
        elif kind == "subsection":
            section_stack["subsection"] = title
            section_stack["subsubsection"] = None
        elif kind == "subsubsection":
            section_stack["subsubsection"] = title


def current_section(section_stack: dict[str, str | None]) -> str | None:
    parts = [
        section_stack["section"],
        section_stack["subsection"],
        section_stack["subsubsection"],
    ]
    visible_parts = [part for part in parts if part]
    if not visible_parts:
        return None
    return " / ".join(visible_parts)


def find_environment_end(
    lines: list[str], start_index: int, environment: str
) -> int:
    end_re = re.compile(rf"\\end\{{{re.escape(environment)}\}}")
    for index in range(start_index, len(lines)):
        if end_re.search(strip_tex_comment(lines[index])):
            return index
    raise ValueError(
        f"Missing \\end{{{environment}}} after line {start_index + 1}"
    )


def make_preview(block_lines: list[str]) -> str:
    for raw_line in block_lines:
        line = strip_tex_comment(raw_line).strip()
        line = remove_begin_commands(line)
        line = END_ANY_RE.sub("", line)
        line = LABEL_RE.sub("", line)
        line = normalise_whitespace(line) or ""
        if line:
            return line[:160]
    return ""


def scan_file(relative_path: str) -> list[ResultEntry]:
    path = REPO_ROOT / relative_path
    lines = path.read_text(encoding="utf-8").splitlines()
    entries: list[ResultEntry] = []
    section_stack: dict[str, str | None] = {
        "section": None,
        "subsection": None,
        "subsubsection": None,
    }

    index = 0
    while index < len(lines):
        line = strip_tex_comment(lines[index])
        update_section_context(line, section_stack)
        match = BEGIN_RE.search(line)
        if not match:
            index += 1
            continue

        environment = match.group("env")
        end_index = find_environment_end(lines, index, environment)
        block_lines = lines[index : end_index + 1]
        block_text = "\n".join(strip_tex_comment(block) for block in block_lines)
        label_match = LABEL_RE.search(block_text)
        title_text, _title_end = extract_optional_argument(line, match.end())
        title = normalise_whitespace(title_text)
        label = label_match.group("label") if label_match else None

        entries.append(
            ResultEntry(
                file=relative_path,
                start_line=index + 1,
                end_line=end_index + 1,
                environment=environment,
                title=title,
                label=label,
                section=current_section(section_stack),
                preview=make_preview(block_lines),
            )
        )
        index = end_index + 1

    return entries


def label_prefix(label: str) -> str:
    if ":" not in label:
        return "<none>"
    return label.split(":", 1)[0]


def entry_location(entry: ResultEntry) -> str:
    return f"{entry.file}:{entry.start_line}-{entry.end_line}"


def duplicate_map(items: list[tuple[str, ResultEntry]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[ResultEntry]] = defaultdict(list)
    for key, entry in items:
        grouped[key].append(entry)
    return {
        key: [asdict(entry) for entry in values]
        for key, values in sorted(grouped.items())
        if len(values) > 1
    }


def build_report(entries: list[ResultEntry]) -> dict[str, Any]:
    by_environment = Counter(entry.environment for entry in entries)
    by_file_environment: dict[str, Counter[str]] = defaultdict(Counter)
    prefix_counts: Counter[str] = Counter()
    labels: list[tuple[str, ResultEntry]] = []
    titles: list[tuple[str, ResultEntry]] = []

    for entry in entries:
        by_file_environment[entry.file][entry.environment] += 1
        if entry.label:
            prefix_counts[label_prefix(entry.label)] += 1
            labels.append((entry.label, entry))
        if entry.title:
            title_key = f"{entry.environment}:{entry.title.casefold()}"
            titles.append((title_key, entry))

    unlabeled_entries = [entry for entry in entries if not entry.label]
    duplicate_labels = duplicate_map(labels)
    repeated_titles = duplicate_map(titles)
    audit_result = "PASS" if not duplicate_labels else "REVIEW"
    if unlabeled_entries:
        audit_result = "REVIEW"

    return {
        "metadata": {
            "proof_status": PROOF_STATUS,
            "theorem_problem_id": THEOREM_PROBLEM_ID,
            "determinism": DETERMINISM,
            "input_files": list(SOURCE_FILES),
            "environments_scanned": list(ENVIRONMENTS),
            "frontier_environments_excluded": list(EXCLUDED_FRONTIER_ENVIRONMENTS),
        },
        "result": {
            "audit_result": audit_result,
            "total_entries": len(entries),
            "labeled_entries": len(entries) - len(unlabeled_entries),
            "unlabeled_entries": len(unlabeled_entries),
            "duplicate_labels": len(duplicate_labels),
            "repeated_titles": len(repeated_titles),
        },
        "counts": {
            "by_environment": dict(sorted(by_environment.items())),
            "by_file_environment": {
                source: dict(sorted(by_file_environment[source].items()))
                for source in SOURCE_FILES
            },
            "label_prefixes": dict(sorted(prefix_counts.items())),
        },
        "unlabeled_entries": [asdict(entry) for entry in unlabeled_entries],
        "duplicate_labels": duplicate_labels,
        "repeated_titles": repeated_titles,
        "entries": [asdict(entry) for entry in entries],
    }


def format_optional(value: str | None) -> str:
    return value if value else "<none>"


def format_text(report: dict[str, Any]) -> str:
    metadata = report["metadata"]
    result = report["result"]
    counts = report["counts"]
    lines: list[str] = [
        "Result environment inventory",
        f"proof_status: {metadata['proof_status']}",
        f"theorem_problem_id: {metadata['theorem_problem_id']}",
        f"determinism: {metadata['determinism']}",
        "input_files:",
    ]
    lines.extend(f"  - {source}" for source in metadata["input_files"])
    lines.append(
        "environments_scanned: "
        + ", ".join(metadata["environments_scanned"])
    )
    lines.append(
        "frontier_environments_excluded: "
        + ", ".join(metadata["frontier_environments_excluded"])
    )
    lines.extend(
        [
            f"audit_result: {result['audit_result']}",
            f"total_entries: {result['total_entries']}",
            f"labeled_entries: {result['labeled_entries']}",
            f"unlabeled_entries: {result['unlabeled_entries']}",
            f"duplicate_labels: {result['duplicate_labels']}",
            f"repeated_titles: {result['repeated_titles']}",
            "counts_by_environment:",
        ]
    )
    for environment, count in counts["by_environment"].items():
        lines.append(f"  - {environment}: {count}")

    lines.append("counts_by_file_environment:")
    for source, source_counts in counts["by_file_environment"].items():
        summary = ", ".join(
            f"{environment}={count}"
            for environment, count in source_counts.items()
        )
        lines.append(f"  - {source}: {summary or '<none>'}")

    lines.append("label_prefixes:")
    for prefix, count in counts["label_prefixes"].items():
        lines.append(f"  - {prefix}: {count}")

    lines.append("unlabeled_entries:")
    if report["unlabeled_entries"]:
        for entry in report["unlabeled_entries"]:
            lines.append(
                "  - "
                f"{entry['file']}:{entry['start_line']} "
                f"{entry['environment']} "
                f"title={format_optional(entry['title'])} "
                f"section={format_optional(entry['section'])}"
            )
    else:
        lines.append("  - <none>")

    lines.append("duplicate_labels:")
    if report["duplicate_labels"]:
        for label, entries in report["duplicate_labels"].items():
            locations = ", ".join(entry_location(ResultEntry(**entry)) for entry in entries)
            lines.append(f"  - {label}: {locations}")
    else:
        lines.append("  - <none>")

    lines.append("repeated_titles:")
    if report["repeated_titles"]:
        for title, entries in report["repeated_titles"].items():
            locations = ", ".join(entry_location(ResultEntry(**entry)) for entry in entries)
            lines.append(f"  - {title}: {locations}")
    else:
        lines.append("  - <none>")

    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inventory theorem-like environments in stable TeX sources."
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format. Defaults to text.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    entries: list[ResultEntry] = []
    for source in SOURCE_FILES:
        entries.extend(scan_file(source))
    report = build_report(entries)
    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(format_text(report))


if __name__ == "__main__":
    main()
