#!/usr/bin/env python3
"""Inventory display-math blocks across stable TeX manuscripts.

Proof status: AUDIT. This deterministic scanner records bracket displays and
named display-math environments, then reports environment counts, local labels,
and numbered display environments that have no local label. It does not compile
or modify stable TeX.
"""

from __future__ import annotations

import argparse
import bisect
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

THEOREM_PROBLEM_ID = "stable-tex-display-math-inventory"
PROOF_STATUS = "AUDIT"
DETERMINISM = "deterministic source scan; no random seed"

DISPLAY_ENVIRONMENTS = (
    "equation",
    "align",
    "gather",
    "multline",
    "alignat",
    "flalign",
)
BEGIN_ENV_RE = re.compile(
    r"\\begin\{(?P<environment>"
    + "|".join(re.escape(env) + r"\*?" for env in DISPLAY_ENVIRONMENTS)
    + r")\}"
)
LABEL_RE = re.compile(r"\\label\{(?P<label>[^{}]+)\}")
BRACKET_OPEN_RE = re.compile(r"\\\[")
BRACKET_CLOSE_RE = re.compile(r"\\\]")


@dataclass(frozen=True)
class LabelEntry:
    label: str
    line: int


@dataclass(frozen=True)
class DisplayBlock:
    file: str
    kind: str
    environment: str
    begin_line: int
    end_line: int | None
    numbered: bool
    labels: list[LabelEntry]
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


def stripped_source(relative_path: str) -> tuple[str, list[int]]:
    path = REPO_ROOT / relative_path
    text = "\n".join(
        strip_tex_comment(line)
        for line in path.read_text(encoding="utf-8").splitlines()
    )
    if text:
        text += "\n"

    line_starts = [0]
    for index, char in enumerate(text):
        if char == "\n" and index + 1 < len(text):
            line_starts.append(index + 1)
    return text, line_starts


def line_number_for(index: int, line_starts: list[int]) -> int:
    return bisect.bisect_right(line_starts, index)


def is_escaped(text: str, index: int) -> bool:
    backslashes = 0
    cursor = index - 1
    while cursor >= 0 and text[cursor] == "\\":
        backslashes += 1
        cursor -= 1
    return backslashes % 2 == 1


def normalise_preview(value: str, limit: int = 120) -> str:
    compact = " ".join(value.split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3].rstrip() + "..."


def labels_in_span(
    text: str,
    start: int,
    end: int,
    line_starts: list[int],
) -> list[LabelEntry]:
    return [
        LabelEntry(
            label=match.group("label"),
            line=line_number_for(match.start(), line_starts),
        )
        for match in LABEL_RE.finditer(text, start, end)
    ]


def scan_named_environments(
    relative_path: str,
    text: str,
    line_starts: list[int],
) -> list[DisplayBlock]:
    blocks: list[DisplayBlock] = []
    for begin_match in BEGIN_ENV_RE.finditer(text):
        environment = begin_match.group("environment")
        end_re = re.compile(r"\\end\{" + re.escape(environment) + r"\}")
        end_match = end_re.search(text, begin_match.end())
        body_end = end_match.start() if end_match else len(text)
        block_end = end_match.end() if end_match else len(text)
        labels = labels_in_span(text, begin_match.start(), block_end, line_starts)

        blocks.append(
            DisplayBlock(
                file=relative_path,
                kind="environment",
                environment=environment,
                begin_line=line_number_for(begin_match.start(), line_starts),
                end_line=(
                    line_number_for(end_match.start(), line_starts)
                    if end_match
                    else None
                ),
                numbered=not environment.endswith("*"),
                labels=labels,
                preview=normalise_preview(text[begin_match.end() : body_end]),
            )
        )
    return blocks


def next_unescaped(
    pattern: re.Pattern[str],
    text: str,
    start: int,
) -> re.Match[str] | None:
    for match in pattern.finditer(text, start):
        if not is_escaped(text, match.start()):
            return match
    return None


def scan_bracket_displays(
    relative_path: str,
    text: str,
    line_starts: list[int],
) -> list[DisplayBlock]:
    blocks: list[DisplayBlock] = []
    search_from = 0
    while True:
        open_match = next_unescaped(BRACKET_OPEN_RE, text, search_from)
        if open_match is None:
            break

        close_match = next_unescaped(BRACKET_CLOSE_RE, text, open_match.end())
        body_end = close_match.start() if close_match else len(text)
        block_end = close_match.end() if close_match else len(text)
        labels = labels_in_span(text, open_match.start(), block_end, line_starts)
        blocks.append(
            DisplayBlock(
                file=relative_path,
                kind="bracket",
                environment="\\[",
                begin_line=line_number_for(open_match.start(), line_starts),
                end_line=(
                    line_number_for(close_match.start(), line_starts)
                    if close_match
                    else None
                ),
                numbered=False,
                labels=labels,
                preview=normalise_preview(text[open_match.end() : body_end]),
            )
        )
        search_from = block_end
    return blocks


def scan_file(relative_path: str) -> list[DisplayBlock]:
    text, line_starts = stripped_source(relative_path)
    blocks = scan_named_environments(relative_path, text, line_starts)
    blocks.extend(scan_bracket_displays(relative_path, text, line_starts))
    return sorted(blocks, key=lambda block: (block.begin_line, block.environment))


def label_dicts(block: DisplayBlock) -> list[dict[str, Any]]:
    return [asdict(label) for label in block.labels]


def block_to_dict(block: DisplayBlock) -> dict[str, Any]:
    data = asdict(block)
    data["labels"] = label_dicts(block)
    return data


def build_report(blocks: list[DisplayBlock]) -> dict[str, Any]:
    counts_by_environment = Counter(block.environment for block in blocks)
    counts_by_file: dict[str, dict[str, int]] = {}
    for source in SOURCE_FILES:
        file_blocks = [block for block in blocks if block.file == source]
        counts_by_file[source] = {
            "total": len(file_blocks),
            "numbered": sum(block.numbered for block in file_blocks),
            "labeled": sum(bool(block.labels) for block in file_blocks),
            "unclosed": sum(block.end_line is None for block in file_blocks),
            "unlabeled_numbered": sum(
                block.numbered and not block.labels for block in file_blocks
            ),
        }

    unlabeled_numbered = [
        block for block in blocks if block.numbered and not block.labels
    ]
    unclosed_blocks = [block for block in blocks if block.end_line is None]
    labeled_blocks = [block for block in blocks if block.labels]
    audit_result = "PASS"
    if unlabeled_numbered or unclosed_blocks:
        audit_result = "REVIEW"

    return {
        "metadata": {
            "proof_status": PROOF_STATUS,
            "theorem_problem_id": THEOREM_PROBLEM_ID,
            "determinism": DETERMINISM,
            "input_files": list(SOURCE_FILES),
            "display_environments": list(DISPLAY_ENVIRONMENTS),
        },
        "result": {
            "audit_result": audit_result,
            "total_display_blocks": len(blocks),
            "bracket_displays": sum(block.kind == "bracket" for block in blocks),
            "environment_displays": sum(
                block.kind == "environment" for block in blocks
            ),
            "numbered_displays": sum(block.numbered for block in blocks),
            "labeled_displays": len(labeled_blocks),
            "unlabeled_numbered_displays": len(unlabeled_numbered),
            "unclosed_display_blocks": len(unclosed_blocks),
        },
        "counts": {
            "by_environment": dict(sorted(counts_by_environment.items())),
            "by_file": counts_by_file,
        },
        "unlabeled_numbered_displays": [
            block_to_dict(block) for block in unlabeled_numbered
        ],
        "unclosed_display_blocks": [block_to_dict(block) for block in unclosed_blocks],
        "labeled_displays": [block_to_dict(block) for block in labeled_blocks],
        "display_blocks": [block_to_dict(block) for block in blocks],
    }


def label_display(block: dict[str, Any]) -> str:
    labels = block["labels"]
    if not labels:
        return "<none>"
    return ",".join(label["label"] for label in labels)


def format_block(block: dict[str, Any]) -> str:
    end_line = block["end_line"] if block["end_line"] is not None else "?"
    return (
        f"{block['file']}:{block['begin_line']}-{end_line} "
        f"{block['environment']} labels={label_display(block)} "
        f"preview={block['preview']!r}"
    )


def format_text(report: dict[str, Any]) -> str:
    metadata = report["metadata"]
    result = report["result"]
    lines = [
        "Display math inventory",
        f"Proof status: {metadata['proof_status']}",
        f"Theorem/problem id: {metadata['theorem_problem_id']}",
        f"Determinism: {metadata['determinism']}",
        f"Audit result: {result['audit_result']}",
        "",
        "Summary:",
        f"  total display blocks: {result['total_display_blocks']}",
        f"  bracket displays: {result['bracket_displays']}",
        f"  environment displays: {result['environment_displays']}",
        f"  numbered displays: {result['numbered_displays']}",
        f"  labeled displays: {result['labeled_displays']}",
        f"  unlabeled numbered displays: {result['unlabeled_numbered_displays']}",
        f"  unclosed display blocks: {result['unclosed_display_blocks']}",
        "",
        "By environment:",
    ]

    for environment, count in report["counts"]["by_environment"].items():
        lines.append(f"  - {environment}: {count}")

    lines.append("")
    lines.append("By file:")
    for source, counts in report["counts"]["by_file"].items():
        lines.append(
            f"  - {source}: {counts['total']} total, {counts['numbered']} "
            f"numbered, {counts['labeled']} labeled, "
            f"{counts['unlabeled_numbered']} unlabeled numbered"
        )

    lines.append("")
    lines.append("Unlabeled numbered displays:")
    unlabeled = report["unlabeled_numbered_displays"]
    if unlabeled:
        for block in unlabeled:
            lines.append(f"  - {format_block(block)}")
    else:
        lines.append("  - none")

    lines.append("")
    lines.append("Unclosed display blocks:")
    unclosed = report["unclosed_display_blocks"]
    if unclosed:
        for block in unclosed:
            lines.append(f"  - {format_block(block)}")
    else:
        lines.append("  - none")

    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Inventory display-math blocks and local labels across stable TeX "
            "manuscripts."
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
    blocks: list[DisplayBlock] = []
    for source in SOURCE_FILES:
        blocks.extend(scan_file(source))

    report = build_report(blocks)
    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(format_text(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
