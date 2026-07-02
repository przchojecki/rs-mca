#!/usr/bin/env python3
"""Inventory proof environments in the stable TeX manuscripts.

Proof status: AUDIT. This script is a deterministic structural scan: it does
not prove or refute any theorem. It records proof blocks, nearby theorem-like
statements, and unmatched proof-bearing statements for later human review.
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
    "tex/slackMCA_v4.tex",
    "tex/cs25_cap_v12.tex",
    "tex/snarks_v5.tex",
    "tex/proximity_blueprint_v3.tex",
)

PROOF_BEARING_ENVIRONMENTS = (
    "theorem",
    "lemma",
    "proposition",
    "corollary",
    "fact",
)

CONTEXT_ENVIRONMENTS = PROOF_BEARING_ENVIRONMENTS + (
    "definition",
    "remark",
    "example",
    "problem",
    "openproblem",
    "conjecture",
    "assumption",
    "designrule",
    "task",
    "milestone",
)

THEOREM_PROBLEM_ID = "stable-tex-proof-environment-inventory"
PROOF_STATUS = "AUDIT"
DETERMINISM = "deterministic; no random seed"

CONTEXT_PATTERN = "|".join(re.escape(env) for env in CONTEXT_ENVIRONMENTS)
CONTEXT_BEGIN_RE = re.compile(
    rf"\\begin\{{(?P<env>{CONTEXT_PATTERN})\}}"
)
PROOF_BEGIN_RE = re.compile(r"\\begin\{proof\}")
PROOF_END_RE = re.compile(r"\\end\{proof\}")
BEGIN_COMMAND_RE = re.compile(r"\\begin\{[^{}]+\}")
END_ANY_RE = re.compile(r"\\end\{[^{}]+\}")
LABEL_RE = re.compile(r"\\label\{(?P<label>[^{}]+)\}")
SECTION_RE = re.compile(
    r"\\(?P<kind>section|subsection|subsubsection)\*?(?:\[[^\]]*\])?\{"
)


@dataclass(frozen=True)
class Statement:
    id: int
    file: str
    start_line: int
    end_line: int
    environment: str
    title: str | None
    label: str | None
    section: str | None
    preview: str
    proof_start_line: int | None = None
    proof_end_line: int | None = None


@dataclass(frozen=True)
class ProofBlock:
    id: int
    file: str
    start_line: int
    end_line: int
    title: str | None
    line_count: int
    section: str | None
    preview: str
    attached_statement_id: int | None
    attached_environment: str | None
    attached_label: str | None
    attached_title: str | None
    attached_statement_start_line: int | None


@dataclass(frozen=True)
class FileScan:
    statements: list[Statement]
    proofs: list[ProofBlock]


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


def clean_preview_line(line: str) -> str:
    line = strip_tex_comment(line).strip()
    line = remove_begin_commands(line)
    line = END_ANY_RE.sub("", line)
    line = LABEL_RE.sub("", line)
    return normalise_whitespace(line) or ""


def make_preview(block_lines: list[str]) -> str:
    for raw_line in block_lines:
        line = clean_preview_line(raw_line)
        if line:
            return line[:160]
    return ""


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


def find_proof_end(lines: list[str], start_index: int) -> int:
    for index in range(start_index, len(lines)):
        if PROOF_END_RE.search(strip_tex_comment(lines[index])):
            return index
    raise ValueError(f"Missing \\end{{proof}} after line {start_index + 1}")


def first_label(block_lines: list[str]) -> str | None:
    block_text = "\n".join(strip_tex_comment(line) for line in block_lines)
    match = LABEL_RE.search(block_text)
    return match.group("label") if match else None


def proof_title(line: str) -> str | None:
    match = PROOF_BEGIN_RE.search(line)
    if not match:
        return None
    title, _end_index = extract_optional_argument(line, match.end())
    return normalise_whitespace(title)


def attach_statement(
    pending_statement: Statement | None,
    proof_start_line: int,
    proof_end_line: int,
) -> Statement | None:
    if pending_statement is None:
        return None
    return Statement(
        id=pending_statement.id,
        file=pending_statement.file,
        start_line=pending_statement.start_line,
        end_line=pending_statement.end_line,
        environment=pending_statement.environment,
        title=pending_statement.title,
        label=pending_statement.label,
        section=pending_statement.section,
        preview=pending_statement.preview,
        proof_start_line=proof_start_line,
        proof_end_line=proof_end_line,
    )


def scan_file(relative_path: str, id_start: int) -> FileScan:
    path = REPO_ROOT / relative_path
    lines = path.read_text(encoding="utf-8").splitlines()
    statements: list[Statement] = []
    proofs: list[ProofBlock] = []
    section_stack: dict[str, str | None] = {
        "section": None,
        "subsection": None,
        "subsubsection": None,
    }
    pending_statement: Statement | None = None
    next_statement_id = id_start
    next_proof_id = id_start

    index = 0
    while index < len(lines):
        line = strip_tex_comment(lines[index])
        update_section_context(line, section_stack)

        proof_match = PROOF_BEGIN_RE.search(line)
        statement_match = CONTEXT_BEGIN_RE.search(line)

        if proof_match:
            end_index = find_proof_end(lines, index)
            block_lines = lines[index : end_index + 1]
            attached = attach_statement(
                pending_statement, index + 1, end_index + 1
            )
            if attached:
                statements[-1] = attached

            proofs.append(
                ProofBlock(
                    id=next_proof_id,
                    file=relative_path,
                    start_line=index + 1,
                    end_line=end_index + 1,
                    title=proof_title(line),
                    line_count=end_index - index + 1,
                    section=current_section(section_stack),
                    preview=make_preview(block_lines),
                    attached_statement_id=attached.id if attached else None,
                    attached_environment=attached.environment if attached else None,
                    attached_label=attached.label if attached else None,
                    attached_title=attached.title if attached else None,
                    attached_statement_start_line=(
                        attached.start_line if attached else None
                    ),
                )
            )
            next_proof_id += 1
            pending_statement = None
            index = end_index + 1
            continue

        if statement_match:
            environment = statement_match.group("env")
            end_index = find_environment_end(lines, index, environment)
            block_lines = lines[index : end_index + 1]
            title_text, _title_end = extract_optional_argument(
                line, statement_match.end()
            )
            statement = Statement(
                id=next_statement_id,
                file=relative_path,
                start_line=index + 1,
                end_line=end_index + 1,
                environment=environment,
                title=normalise_whitespace(title_text),
                label=first_label(block_lines),
                section=current_section(section_stack),
                preview=make_preview(block_lines),
            )
            next_statement_id += 1
            if environment in PROOF_BEARING_ENVIRONMENTS:
                pending_statement = statement
            else:
                pending_statement = None
            statements.append(statement)
            index = end_index + 1
            continue

        if line.strip():
            pending_statement = None
        index += 1

    return FileScan(statements=statements, proofs=proofs)


def proof_status(statement: Statement) -> str:
    if statement.environment not in PROOF_BEARING_ENVIRONMENTS:
        return "not-proof-bearing"
    return "proved-locally" if statement.proof_start_line else "no-attached-proof"


def build_report(file_scans: list[FileScan]) -> dict[str, Any]:
    statements = [
        statement
        for file_scan in file_scans
        for statement in file_scan.statements
    ]
    proofs = [proof for file_scan in file_scans for proof in file_scan.proofs]
    proof_bearing = [
        statement
        for statement in statements
        if statement.environment in PROOF_BEARING_ENVIRONMENTS
    ]
    no_attached_proof = [
        statement
        for statement in proof_bearing
        if statement.proof_start_line is None
    ]
    orphan_proofs = [
        proof for proof in proofs if proof.attached_statement_id is None
    ]

    statements_by_env = Counter(statement.environment for statement in statements)
    proof_bearing_by_env = Counter(
        statement.environment for statement in proof_bearing
    )
    proofs_by_file: dict[str, int] = {source: 0 for source in SOURCE_FILES}
    statements_by_file_env: dict[str, Counter[str]] = defaultdict(Counter)

    for statement in statements:
        statements_by_file_env[statement.file][statement.environment] += 1
    for proof in proofs:
        proofs_by_file[proof.file] += 1

    audit_result = "PASS"
    if no_attached_proof or orphan_proofs:
        audit_result = "REVIEW"

    return {
        "metadata": {
            "proof_status": PROOF_STATUS,
            "theorem_problem_id": THEOREM_PROBLEM_ID,
            "determinism": DETERMINISM,
            "input_files": list(SOURCE_FILES),
            "proof_bearing_environments": list(PROOF_BEARING_ENVIRONMENTS),
            "context_environments": list(CONTEXT_ENVIRONMENTS),
        },
        "result": {
            "audit_result": audit_result,
            "proof_bearing_statements": len(proof_bearing),
            "proof_blocks": len(proofs),
            "attached_proofs": len(proofs) - len(orphan_proofs),
            "orphan_proofs": len(orphan_proofs),
            "statements_without_attached_proof": len(no_attached_proof),
        },
        "counts": {
            "statements_by_environment": dict(sorted(statements_by_env.items())),
            "proof_bearing_by_environment": dict(
                sorted(proof_bearing_by_env.items())
            ),
            "proofs_by_file": dict(sorted(proofs_by_file.items())),
            "statements_by_file_environment": {
                source: dict(sorted(statements_by_file_env[source].items()))
                for source in SOURCE_FILES
            },
        },
        "statements_without_attached_proof": [
            asdict(statement) | {"local_proof_status": proof_status(statement)}
            for statement in no_attached_proof
        ],
        "orphan_proofs": [asdict(proof) for proof in orphan_proofs],
        "proofs": [asdict(proof) for proof in proofs],
        "statements": [
            asdict(statement) | {"local_proof_status": proof_status(statement)}
            for statement in statements
        ],
    }


def format_optional(value: str | None) -> str:
    return value if value else "<none>"


def format_text(report: dict[str, Any]) -> str:
    metadata = report["metadata"]
    result = report["result"]
    counts = report["counts"]
    lines: list[str] = [
        "Proof environment inventory",
        f"proof_status: {metadata['proof_status']}",
        f"theorem_problem_id: {metadata['theorem_problem_id']}",
        f"determinism: {metadata['determinism']}",
        "input_files:",
    ]
    lines.extend(f"  - {source}" for source in metadata["input_files"])
    lines.append(
        "proof_bearing_environments: "
        + ", ".join(metadata["proof_bearing_environments"])
    )
    lines.extend(
        [
            f"audit_result: {result['audit_result']}",
            f"proof_bearing_statements: {result['proof_bearing_statements']}",
            f"proof_blocks: {result['proof_blocks']}",
            f"attached_proofs: {result['attached_proofs']}",
            f"orphan_proofs: {result['orphan_proofs']}",
            "statements_without_attached_proof: "
            f"{result['statements_without_attached_proof']}",
            "proof_bearing_by_environment:",
        ]
    )
    for environment, count in counts["proof_bearing_by_environment"].items():
        lines.append(f"  - {environment}: {count}")

    lines.append("proofs_by_file:")
    for source, count in counts["proofs_by_file"].items():
        lines.append(f"  - {source}: {count}")

    lines.append("statements_without_attached_proof:")
    if report["statements_without_attached_proof"]:
        for statement in report["statements_without_attached_proof"]:
            lines.append(
                "  - "
                f"{statement['file']}:{statement['start_line']} "
                f"{statement['environment']} "
                f"label={format_optional(statement['label'])} "
                f"title={format_optional(statement['title'])}"
            )
    else:
        lines.append("  - <none>")

    lines.append("orphan_proofs:")
    if report["orphan_proofs"]:
        for proof in report["orphan_proofs"]:
            lines.append(
                "  - "
                f"{proof['file']}:{proof['start_line']} "
                f"title={format_optional(proof['title'])} "
                f"section={format_optional(proof['section'])}"
            )
    else:
        lines.append("  - <none>")

    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inventory proof environments in stable TeX sources."
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
    file_scans: list[FileScan] = []
    next_id = 1
    for source in SOURCE_FILES:
        file_scan = scan_file(source, next_id)
        file_scans.append(file_scan)
        next_id += len(file_scan.statements) + len(file_scan.proofs) + 1

    report = build_report(file_scans)
    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(format_text(report))


if __name__ == "__main__":
    main()
