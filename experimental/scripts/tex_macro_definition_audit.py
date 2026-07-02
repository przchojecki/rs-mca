#!/usr/bin/env python3
"""Audit TeX macro definition drift across stable manuscripts.

Proof status: AUDIT.

The manuscripts are standalone files, so differing local macro definitions are
not automatically wrong.  This script records those differences explicitly so
notation cleanup can distinguish intentional local choices from accidental
drift.
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
PROOF_STATUS = "AUDIT"
PROBLEM_ID = "Suite-level TeX macro definition drift audit"


NEWCOMMAND_RE = re.compile(
    r"\\newcommand\{\\(?P<command>[A-Za-z]+)\}"
    r"(?:\[(?P<arity>[0-9]+)\])?"
    r"\{(?P<body>.*)\}\s*$"
)
DECLARE_OPERATOR_RE = re.compile(
    r"\\DeclareMathOperator\*?\{\\(?P<command>[A-Za-z]+)\}\{(?P<body>.*)\}\s*$"
)


@dataclass(frozen=True)
class MacroDefinition:
    file: str
    line: int
    command: str
    kind: str
    arity: int
    body: str
    normalized_body: str
    snippet: str


@dataclass(frozen=True)
class MacroVariant:
    command: str
    kind: str
    arity: int
    normalized_body: str
    locations: tuple[str, ...]


@dataclass(frozen=True)
class MacroDrift:
    command: str
    variants: tuple[MacroVariant, ...]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_lines(root: Path, relative_path: str) -> list[str]:
    return (root / relative_path).read_text(encoding="utf-8").splitlines()


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


def normalize_body(body: str) -> str:
    return clean_snippet(body)


def parse_macro_line(
    relative_path: str,
    line_no: int,
    raw_line: str,
) -> MacroDefinition | None:
    line = strip_comment(raw_line)
    snippet = clean_snippet(line)
    match = NEWCOMMAND_RE.search(line)
    if match:
        body = match.group("body")
        return MacroDefinition(
            file=relative_path,
            line=line_no,
            command=match.group("command"),
            kind="newcommand",
            arity=int(match.group("arity") or 0),
            body=body,
            normalized_body=normalize_body(body),
            snippet=snippet,
        )
    match = DECLARE_OPERATOR_RE.search(line)
    if match:
        body = match.group("body")
        return MacroDefinition(
            file=relative_path,
            line=line_no,
            command=match.group("command"),
            kind="DeclareMathOperator",
            arity=0,
            body=body,
            normalized_body=normalize_body(body),
            snippet=snippet,
        )
    return None


def collect_definitions() -> list[MacroDefinition]:
    root = repo_root()
    definitions: list[MacroDefinition] = []
    for relative_path in TEX_FILES:
        for line_no, raw_line in enumerate(read_lines(root, relative_path), start=1):
            definition = parse_macro_line(relative_path, line_no, raw_line)
            if definition is not None:
                definitions.append(definition)
    return definitions


def group_by_command(
    definitions: list[MacroDefinition],
) -> dict[str, list[MacroDefinition]]:
    grouped: dict[str, list[MacroDefinition]] = {}
    for definition in definitions:
        grouped.setdefault(definition.command, []).append(definition)
    return grouped


def variant_key(definition: MacroDefinition) -> tuple[str, int, str]:
    return definition.kind, definition.arity, definition.normalized_body


def macro_variants(command: str, definitions: list[MacroDefinition]) -> list[MacroVariant]:
    grouped: dict[tuple[str, int, str], list[str]] = {}
    for definition in definitions:
        grouped.setdefault(variant_key(definition), []).append(
            f"{definition.file}:{definition.line}"
        )
    return [
        MacroVariant(
            command=command,
            kind=kind,
            arity=arity,
            normalized_body=body,
            locations=tuple(locations),
        )
        for (kind, arity, body), locations in sorted(grouped.items())
    ]


def drift_entries(definitions: list[MacroDefinition]) -> list[MacroDrift]:
    entries: list[MacroDrift] = []
    for command, command_defs in sorted(group_by_command(definitions).items()):
        variants = macro_variants(command, command_defs)
        if len(variants) > 1:
            entries.append(MacroDrift(command=command, variants=tuple(variants)))
    return entries


def duplicate_definitions_same_file(
    definitions: list[MacroDefinition],
) -> list[MacroDrift]:
    entries: list[MacroDrift] = []
    grouped: dict[tuple[str, str], list[MacroDefinition]] = {}
    for definition in definitions:
        grouped.setdefault((definition.file, definition.command), []).append(definition)
    for (_file_name, command), command_defs in sorted(grouped.items()):
        if len(command_defs) <= 1:
            continue
        entries.append(
            MacroDrift(command=command, variants=tuple(macro_variants(command, command_defs)))
        )
    return entries


def count_by_file(definitions: list[MacroDefinition]) -> dict[str, int]:
    counts = {file_name: 0 for file_name in TEX_FILES}
    for definition in definitions:
        counts[definition.file] += 1
    return counts


def count_by_kind(definitions: list[MacroDefinition]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for definition in definitions:
        counts[definition.kind] = counts.get(definition.kind, 0) + 1
    return dict(sorted(counts.items()))


def cross_file_command_count(definitions: list[MacroDefinition]) -> int:
    count = 0
    for command_defs in group_by_command(definitions).values():
        if len({definition.file for definition in command_defs}) > 1:
            count += 1
    return count


def build_notes(
    drifts: list[MacroDrift],
    same_file_duplicates: list[MacroDrift],
) -> list[str]:
    notes: list[str] = []
    if drifts:
        notes.append(
            f"{len(drifts)} macro commands have more than one definition variant."
        )
    else:
        notes.append("No cross-manuscript macro definition drift was found.")
    if same_file_duplicates:
        notes.append(
            f"{len(same_file_duplicates)} macro commands are defined more than once "
            "inside a single manuscript."
        )
    notes.append(
        "This is a syntactic audit only; standalone manuscripts may intentionally "
        "define local notation differently."
    )
    return notes


def build_report() -> dict[str, object]:
    definitions = collect_definitions()
    drifts = drift_entries(definitions)
    same_file_duplicates = duplicate_definitions_same_file(definitions)
    return {
        "proof_status": PROOF_STATUS,
        "theorem_or_problem_id": PROBLEM_ID,
        "input_parameters": {
            "source_files": TEX_FILES,
            "definition_patterns": {
                "newcommand": NEWCOMMAND_RE.pattern,
                "DeclareMathOperator": DECLARE_OPERATOR_RE.pattern,
            },
        },
        "exact_object": {
            "audit_type": "line-based TeX macro definition scan",
            "random_seed": None,
        },
        "result": {
            "total_definitions": len(definitions),
            "unique_commands": len(group_by_command(definitions)),
            "cross_file_commands": cross_file_command_count(definitions),
            "drifted_command_count": len(drifts),
            "same_file_duplicate_command_count": len(same_file_duplicates),
            "counts_by_file": count_by_file(definitions),
            "counts_by_kind": count_by_kind(definitions),
            "notes": build_notes(drifts, same_file_duplicates),
        },
        "proof_certificate": {
            "definitions": [asdict(definition) for definition in definitions],
            "drifted_commands": [asdict(entry) for entry in drifts],
            "same_file_duplicate_commands": [
                asdict(entry) for entry in same_file_duplicates
            ],
        },
    }


def print_drift_entries(report: dict[str, object], limit: int = 24) -> None:
    drifts = report["proof_certificate"]["drifted_commands"]
    print("")
    print("Drifted macro definitions:")
    if not drifts:
        print("  none")
        return
    for entry in drifts[:limit]:
        print(f"  \\{entry['command']}: {len(entry['variants'])} variants")
        for variant in entry["variants"]:
            locations = ", ".join(variant["locations"])
            print(
                f"    arity={variant['arity']} body={variant['normalized_body']} "
                f"[{locations}]"
            )
    if len(drifts) > limit:
        print(f"  ... {len(drifts) - limit} more; use --format json for full output")


def print_same_file_duplicates(report: dict[str, object]) -> None:
    duplicates = report["proof_certificate"]["same_file_duplicate_commands"]
    print("")
    print("Same-file duplicate macro definitions:")
    if not duplicates:
        print("  none")
        return
    for entry in duplicates:
        print(f"  \\{entry['command']}: {len(entry['variants'])} variants")


def print_text(report: dict[str, object]) -> None:
    result = report["result"]
    print("TeX macro definition audit")
    print(f"Proof status: {report['proof_status']}")
    print(f"Theorem/problem ID: {report['theorem_or_problem_id']}")
    print("Input params:")
    for source in report["input_parameters"]["source_files"]:
        print(f"  source_file={source}")
    print("Exact object: line-based TeX macro definition scan; random_seed=None")
    print("")
    print("Summary:")
    print(f"  total_definitions={result['total_definitions']}")
    print(f"  unique_commands={result['unique_commands']}")
    print(f"  cross_file_commands={result['cross_file_commands']}")
    print(f"  drifted_commands={result['drifted_command_count']}")
    print(f"  same_file_duplicate_commands={result['same_file_duplicate_command_count']}")
    print("")
    print("Counts by file:")
    for file_name, count in result["counts_by_file"].items():
        print(f"  {file_name}: {count}")
    print("")
    print("Counts by definition kind:")
    for kind, count in result["counts_by_kind"].items():
        print(f"  {kind}: {count}")
    print_drift_entries(report)
    print_same_file_duplicates(report)
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
