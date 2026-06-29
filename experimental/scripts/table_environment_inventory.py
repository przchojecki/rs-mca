#!/usr/bin/env python3
"""Inventory table-like environments in the stable TeX manuscripts.

Proof status: AUDIT. This deterministic scanner records table, longtable,
tabular, and tabularx blocks, along with captions, labels, section context, and
status vocabulary. It does not modify stable TeX.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
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

TABLE_ENVIRONMENTS = (
    "table",
    "longtable",
    "tabular",
    "tabularx",
)

CAPTION_ENVIRONMENTS = ("table", "longtable")
STATUS_WORDS = (
    "proved",
    "conditional",
    "conjectural",
    "experimental",
    "audit",
    "counterexample",
    "verified",
    "open",
)

THEOREM_PROBLEM_ID = "stable-tex-table-environment-inventory"
PROOF_STATUS = "AUDIT"
DETERMINISM = "deterministic source scan; no random seed"

ENV_PATTERN = "|".join(re.escape(environment) for environment in TABLE_ENVIRONMENTS)
BEGIN_RE = re.compile(rf"\\begin\{{(?P<env>{ENV_PATTERN})\}}")
LABEL_RE = re.compile(r"\\label\{(?P<label>[^{}]+)\}")
CAPTION_RE = re.compile(r"\\caption(?:\[[^\]]*\])?\{")
SECTION_RE = re.compile(
    r"\\(?P<kind>section|subsection|subsubsection)\*?(?:\[[^\]]*\])?\{"
)


@dataclass(frozen=True)
class TableEntry:
    file: str
    start_line: int
    end_line: int
    environment: str
    section: str | None
    caption: str | None
    label: str | None
    status_words: list[str]
    preview: str


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


def normalise_whitespace(value: str | None) -> str | None:
    if value is None:
        return None
    return " ".join(value.split())


def find_matching_brace(text: str, opening_index: int) -> int | None:
    depth = 0
    for index in range(opening_index, len(text)):
        char = text[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return index
    return None


def extract_braced_argument(text: str, opening_index: int) -> str | None:
    closing_index = find_matching_brace(text, opening_index)
    if closing_index is None:
        return None
    return text[opening_index + 1 : closing_index]


def extract_caption(block_text: str) -> str | None:
    match = CAPTION_RE.search(block_text)
    if not match:
        return None
    return normalise_whitespace(
        extract_braced_argument(block_text, match.end() - 1)
    )


def first_label(block_text: str) -> str | None:
    match = LABEL_RE.search(block_text)
    if not match:
        return None
    return match.group("label")


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
        line = normalise_whitespace(strip_tex_comment(raw_line).strip()) or ""
        if not line:
            continue
        if line.startswith(r"\begin") or line.startswith(r"\end"):
            continue
        return line[:160]
    return ""


def status_words(block_text: str) -> list[str]:
    lower_text = block_text.lower()
    return [
        word for word in STATUS_WORDS if re.search(rf"\b{word}\b", lower_text)
    ]


def scan_file(relative_path: str) -> list[TableEntry]:
    path = REPO_ROOT / relative_path
    lines = path.read_text(encoding="utf-8").splitlines()
    entries: list[TableEntry] = []
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
        entries.append(
            TableEntry(
                file=relative_path,
                start_line=index + 1,
                end_line=end_index + 1,
                environment=environment,
                section=current_section(section_stack),
                caption=extract_caption(block_text),
                label=first_label(block_text),
                status_words=status_words(block_text),
                preview=make_preview(block_lines),
            )
        )
        index += 1

    return entries


def build_report(entries: list[TableEntry]) -> dict[str, Any]:
    by_environment = Counter(entry.environment for entry in entries)
    by_file = Counter(entry.file for entry in entries)
    caption_capable = [
        entry for entry in entries if entry.environment in CAPTION_ENVIRONMENTS
    ]
    missing_caption = [entry for entry in caption_capable if not entry.caption]
    missing_label = [entry for entry in caption_capable if not entry.label]
    with_status_words = [entry for entry in entries if entry.status_words]
    label_counts = Counter(entry.label for entry in entries if entry.label)
    duplicate_labels = {
        label: [
            asdict(entry)
            for entry in entries
            if entry.label == label
        ]
        for label, count in sorted(label_counts.items())
        if count > 1
    }
    audit_result = "PASS"
    if missing_caption or missing_label or duplicate_labels:
        audit_result = "REVIEW"

    return {
        "metadata": {
            "proof_status": PROOF_STATUS,
            "theorem_problem_id": THEOREM_PROBLEM_ID,
            "determinism": DETERMINISM,
            "input_files": list(SOURCE_FILES),
            "table_environments": list(TABLE_ENVIRONMENTS),
            "caption_environments": list(CAPTION_ENVIRONMENTS),
            "status_words": list(STATUS_WORDS),
        },
        "result": {
            "audit_result": audit_result,
            "total_entries": len(entries),
            "caption_capable_entries": len(caption_capable),
            "missing_caption": len(missing_caption),
            "missing_label": len(missing_label),
            "entries_with_status_words": len(with_status_words),
            "duplicate_labels": len(duplicate_labels),
        },
        "counts": {
            "by_environment": dict(sorted(by_environment.items())),
            "by_file": dict(sorted(by_file.items())),
        },
        "missing_caption": [asdict(entry) for entry in missing_caption],
        "missing_label": [asdict(entry) for entry in missing_label],
        "entries_with_status_words": [
            asdict(entry) for entry in with_status_words
        ],
        "duplicate_labels": duplicate_labels,
        "entries": [asdict(entry) for entry in entries],
    }


def format_optional(value: str | None) -> str:
    return value if value else "<none>"


def format_text(report: dict[str, Any]) -> str:
    metadata = report["metadata"]
    result = report["result"]
    counts = report["counts"]
    lines: list[str] = [
        "Table environment inventory",
        f"proof_status: {metadata['proof_status']}",
        f"theorem_problem_id: {metadata['theorem_problem_id']}",
        f"determinism: {metadata['determinism']}",
        "input_files:",
    ]
    lines.extend(f"  - {source}" for source in metadata["input_files"])
    lines.append(
        "table_environments: " + ", ".join(metadata["table_environments"])
    )
    lines.extend(
        [
            f"audit_result: {result['audit_result']}",
            f"total_entries: {result['total_entries']}",
            f"caption_capable_entries: {result['caption_capable_entries']}",
            f"missing_caption: {result['missing_caption']}",
            f"missing_label: {result['missing_label']}",
            f"entries_with_status_words: {result['entries_with_status_words']}",
            f"duplicate_labels: {result['duplicate_labels']}",
            "counts_by_environment:",
        ]
    )
    for environment, count in counts["by_environment"].items():
        lines.append(f"  - {environment}: {count}")
    lines.append("counts_by_file:")
    for source, count in counts["by_file"].items():
        lines.append(f"  - {source}: {count}")

    lines.append("caption_capable_review:")
    reviewed = report["missing_caption"] or report["missing_label"]
    if not reviewed:
        lines.append("  - <none>")
    else:
        seen: set[tuple[str, int, str]] = set()
        for key, entries in (
            ("missing_caption", report["missing_caption"]),
            ("missing_label", report["missing_label"]),
        ):
            for entry in entries:
                identity = (entry["file"], entry["start_line"], key)
                if identity in seen:
                    continue
                seen.add(identity)
                lines.append(
                    "  - "
                    f"{entry['file']}:{entry['start_line']} "
                    f"{entry['environment']} {key} "
                    f"label={format_optional(entry['label'])}"
                )

    lines.append("entries_with_status_words:")
    if not report["entries_with_status_words"]:
        lines.append("  - <none>")
    else:
        for entry in report["entries_with_status_words"]:
            lines.append(
                "  - "
                f"{entry['file']}:{entry['start_line']} "
                f"{entry['environment']} "
                f"status={','.join(entry['status_words'])} "
                f"label={format_optional(entry['label'])}"
            )

    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inventory table-like environments in stable TeX sources."
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
    entries: list[TableEntry] = []
    for source in SOURCE_FILES:
        entries.extend(scan_file(source))
    report = build_report(entries)
    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(format_text(report))


if __name__ == "__main__":
    main()
