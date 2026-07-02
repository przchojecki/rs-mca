#!/usr/bin/env python3
"""Audit field-ledger vocabulary in the manuscripts and agent guide.

Proof status: AUDIT.

The project guide says not to merge q_gen, q_line, and q_chal without a theorem.
This script gives a deterministic text audit of that vocabulary.  It checks that
the Paper C and blueprint anchors for field accounting are present, counts the
ledger macros, and records field-accounting phrase hits for review.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path


SOURCE_FILES = (
    "agents.md",
    "tex/snarks_v5.tex",
    "tex/proximity_blueprint_v3.tex",
    "tex/slackMCA_v4.tex",
    "tex/cs25_cap_v12.tex",
)
PROOF_STATUS = "AUDIT"
PROBLEM_ID = "Paper C field-ledger hygiene / agent-guide rule 2"

LEDGER_MACROS = ("qgen", "qline", "qchal", "qarith")
MACRO_LABELS = {
    "qgen": "generated field",
    "qline": "line field",
    "qchal": "challenge field",
    "qarith": "arithmetic field",
}
PLAIN_ALIASES = {
    "qgen": ("q_gen",),
    "qline": ("q_line",),
    "qchal": ("q_chal",),
    "qarith": ("q_arith",),
}

PHRASE_PATTERNS = {
    "generated_field": (
        r"\bgenerated field\b",
        r"\bgenerated-field\b",
        r"\bfield of definition\b",
    ),
    "line_field": (
        r"\bline field\b",
        r"\bline or challenge field\b",
        r"\bfield from which the line challenge\b",
    ),
    "challenge_field": (
        r"\bchallenge field\b",
        r"\bchallenge fields\b",
        r"\bverifier challenge field\b",
    ),
    "extension_field": (
        r"\bextension field\b",
        r"\bextension fields\b",
        r"\bextension challenge\b",
        r"\bextension challenges\b",
        r"\bextension-line\b",
        r"\bextension-code\b",
    ),
    "double_credit_guard": (
        r"\bdouble-credit",
        r"\bNo automatic\b",
        r"\bcannot simply be divided\b",
        r"\bcannot divide\b",
        r"\bdoes not improve\b",
        r"\bdo not increase\b",
        r"\bmust include\b",
    ),
}

ANCHORS = (
    {
        "id": "paper_c_qgen_macro",
        "file": "tex/snarks_v5.tex",
        "description": "Paper C defines the generated-field macro",
        "patterns": (r"\\newcommand\{\\qgen\}",),
    },
    {
        "id": "paper_c_qline_macro",
        "file": "tex/snarks_v5.tex",
        "description": "Paper C defines the line-field macro",
        "patterns": (r"\\newcommand\{\\qline\}",),
    },
    {
        "id": "paper_c_qchal_macro",
        "file": "tex/snarks_v5.tex",
        "description": "Paper C defines the challenge-field macro",
        "patterns": (r"\\newcommand\{\\qchal\}",),
    },
    {
        "id": "paper_c_qarith_macro",
        "file": "tex/snarks_v5.tex",
        "description": "Paper C defines the arithmetic-field macro",
        "patterns": (r"\\newcommand\{\\qarith\}",),
    },
    {
        "id": "paper_c_field_section",
        "file": "tex/snarks_v5.tex",
        "description": "Paper C has a fields and challenge-accounting section",
        "patterns": (r"\\label\{sec:fields\}",),
    },
    {
        "id": "paper_c_no_double_credit_rule",
        "file": "tex/snarks_v5.tex",
        "description": "Paper C states the no-double-crediting rule",
        "patterns": (r"\\label\{rule:no-double-credit\}",),
    },
    {
        "id": "paper_c_no_qchal_substitution_remark",
        "file": "tex/snarks_v5.tex",
        "description": "Paper C warns against automatic q_chal substitution",
        "patterns": (r"\\label\{rem:no-substitution\}",),
    },
    {
        "id": "paper_c_certificate_tuple",
        "file": "tex/snarks_v5.tex",
        "description": "Paper C certificate tuple carries q_arith, q_gen, and q_line",
        "patterns": (r"\\cert=\(\\qarith,\\qgen,\\qline",),
    },
    {
        "id": "paper_c_entropy_uses_qgen",
        "file": "tex/snarks_v5.tex",
        "description": "Paper C entropy ledger uses q_gen",
        "patterns": (r"\\entres\(a;\\qgen\)", r"\\label\{eq:entropy-ledger\}"),
    },
    {
        "id": "paper_c_list_budget_uses_qline",
        "file": "tex/snarks_v5.tex",
        "description": "Paper C list-over-field budget uses q_line",
        "patterns": (r"\\widehat L_\{\\mu\}\(\\delta\)/\\qline",),
    },
    {
        "id": "blueprint_field_macros",
        "file": "tex/proximity_blueprint_v3.tex",
        "description": "Blueprint defines q_gen, q_line, and q_chal macros",
        "patterns": (
            r"\\newcommand\{\\qgen\}",
            r"\\newcommand\{\\qline\}",
            r"\\newcommand\{\\qchal\}",
        ),
    },
    {
        "id": "blueprint_field_definition",
        "file": "tex/proximity_blueprint_v3.tex",
        "description": "Blueprint defines generated field, line field, and list arity",
        "patterns": (r"\\label\{def:fields\}",),
    },
    {
        "id": "blueprint_reserve_checklist",
        "file": "tex/proximity_blueprint_v3.tex",
        "description": "Blueprint reserve checklist includes field-ledger terms",
        "patterns": (r"\\label\{task:reserve-checklist\}",),
    },
    {
        "id": "blueprint_no_qline_qchal_assumption",
        "file": "tex/proximity_blueprint_v3.tex",
        "description": "Blueprint warns not to assume q_line equals q_chal",
        "patterns": (r"Do not assume .*\\qline=\\qchal",),
    },
)


@dataclass(frozen=True)
class MacroHit:
    file: str
    line: int
    macro: str
    role: str
    snippet: str


@dataclass(frozen=True)
class PhraseHit:
    file: str
    line: int
    phrase_group: str
    matched_text: str
    has_explicit_ledger_macro: bool
    snippet: str


@dataclass(frozen=True)
class AnchorResult:
    id: str
    file: str
    description: str
    found: bool
    matched_lines: tuple[int, ...]
    missing_patterns: tuple[str, ...]


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


def macro_pattern(macro: str) -> re.Pattern[str]:
    alternatives = [rf"\\{re.escape(macro)}(?![A-Za-z])"]
    alternatives.extend(rf"\b{re.escape(alias)}\b" for alias in PLAIN_ALIASES[macro])
    return re.compile("|".join(alternatives))


def macro_role(line: str, macro: str) -> str:
    if re.search(rf"\\newcommand\{{\\{re.escape(macro)}\}}", line):
        return "definition"
    return "use"


def has_ledger_macro(line: str) -> bool:
    return any(macro_pattern(macro).search(line) for macro in LEDGER_MACROS)


def collect_macro_hits(root: Path) -> list[MacroHit]:
    hits: list[MacroHit] = []
    patterns = {macro: macro_pattern(macro) for macro in LEDGER_MACROS}
    for relative_path in SOURCE_FILES:
        for line_no, raw_line in enumerate(read_lines(root, relative_path), start=1):
            line = strip_comment(raw_line)
            for macro, pattern in patterns.items():
                if not pattern.search(line):
                    continue
                hits.append(
                    MacroHit(
                        file=relative_path,
                        line=line_no,
                        macro=macro,
                        role=macro_role(line, macro),
                        snippet=clean_snippet(line),
                    )
                )
    return hits


def collect_phrase_hits(root: Path) -> list[PhraseHit]:
    hits: list[PhraseHit] = []
    for relative_path in SOURCE_FILES:
        for line_no, raw_line in enumerate(read_lines(root, relative_path), start=1):
            line = strip_comment(raw_line)
            for phrase_group, patterns in PHRASE_PATTERNS.items():
                for pattern in patterns:
                    for match in re.finditer(pattern, line, flags=re.IGNORECASE):
                        hits.append(
                            PhraseHit(
                                file=relative_path,
                                line=line_no,
                                phrase_group=phrase_group,
                                matched_text=match.group(0),
                                has_explicit_ledger_macro=has_ledger_macro(line),
                                snippet=clean_snippet(line),
                            )
                        )
    return hits


def check_anchor(root: Path, anchor: dict[str, object]) -> AnchorResult:
    lines = read_lines(root, str(anchor["file"]))
    matched_lines: list[int] = []
    missing_patterns: list[str] = []
    for pattern in anchor["patterns"]:
        pattern_lines = [
            line_no
            for line_no, raw_line in enumerate(lines, start=1)
            if re.search(str(pattern), strip_comment(raw_line))
        ]
        if pattern_lines:
            matched_lines.extend(pattern_lines)
        else:
            missing_patterns.append(str(pattern))
    return AnchorResult(
        id=str(anchor["id"]),
        file=str(anchor["file"]),
        description=str(anchor["description"]),
        found=not missing_patterns,
        matched_lines=tuple(sorted(set(matched_lines))),
        missing_patterns=tuple(missing_patterns),
    )


def check_anchors(root: Path) -> list[AnchorResult]:
    return [check_anchor(root, anchor) for anchor in ANCHORS]


def count_macros_by_file(hits: list[MacroHit]) -> dict[str, dict[str, int]]:
    counts: dict[str, dict[str, int]] = {
        file_name: {macro: 0 for macro in LEDGER_MACROS}
        for file_name in SOURCE_FILES
    }
    for hit in hits:
        counts.setdefault(hit.file, {macro: 0 for macro in LEDGER_MACROS})
        counts[hit.file][hit.macro] += 1
    return counts


def count_phrases_by_group(hits: list[PhraseHit]) -> dict[str, int]:
    counts = {phrase_group: 0 for phrase_group in PHRASE_PATTERNS}
    for hit in hits:
        counts[hit.phrase_group] += 1
    return counts


def macro_definition_summary(hits: list[MacroHit]) -> dict[str, list[str]]:
    definitions: dict[str, list[str]] = {macro: [] for macro in LEDGER_MACROS}
    for hit in hits:
        if hit.role == "definition":
            definitions[hit.macro].append(f"{hit.file}:{hit.line}")
    return definitions


def build_notes(
    anchors: list[AnchorResult],
    phrase_hits: list[PhraseHit],
) -> list[str]:
    notes: list[str] = []
    missing = [anchor for anchor in anchors if not anchor.found]
    if missing:
        notes.append(f"{len(missing)} required field-ledger anchors are missing.")
    else:
        notes.append("All required Paper C and blueprint field-ledger anchors were found.")
    soft_hits = [
        hit for hit in phrase_hits
        if not hit.has_explicit_ledger_macro
        and hit.phrase_group in {"challenge_field", "extension_field"}
    ]
    if soft_hits:
        notes.append(
            f"{len(soft_hits)} challenge/extension-field phrase hits lack an explicit "
            "q_gen/q_line/q_chal macro on the same line; review only, not an error."
        )
    notes.append("This is a text audit only; it does not prove field-transfer statements.")
    return notes


def build_report() -> dict[str, object]:
    root = repo_root()
    macro_hits = collect_macro_hits(root)
    phrase_hits = collect_phrase_hits(root)
    anchors = check_anchors(root)
    soft_phrase_hits = [
        hit for hit in phrase_hits
        if not hit.has_explicit_ledger_macro
        and hit.phrase_group in {"challenge_field", "extension_field"}
    ]
    return {
        "proof_status": PROOF_STATUS,
        "theorem_or_problem_id": PROBLEM_ID,
        "input_parameters": {
            "source_files": SOURCE_FILES,
            "ledger_macros": LEDGER_MACROS,
            "macro_labels": MACRO_LABELS,
            "phrase_groups": tuple(PHRASE_PATTERNS),
        },
        "exact_object": {
            "audit_type": "line-based field-ledger vocabulary scan",
            "random_seed": None,
        },
        "result": {
            "macro_counts_by_file": count_macros_by_file(macro_hits),
            "macro_definitions": macro_definition_summary(macro_hits),
            "phrase_counts_by_group": count_phrases_by_group(phrase_hits),
            "anchor_count": len(anchors),
            "missing_anchor_count": sum(1 for anchor in anchors if not anchor.found),
            "soft_phrase_review_count": len(soft_phrase_hits),
            "notes": build_notes(anchors, phrase_hits),
        },
        "proof_certificate": {
            "macro_hits": [asdict(hit) for hit in macro_hits],
            "phrase_hits": [asdict(hit) for hit in phrase_hits],
            "soft_phrase_review_hits": [asdict(hit) for hit in soft_phrase_hits],
            "anchor_results": [asdict(anchor) for anchor in anchors],
        },
    }


def print_anchor_results(report: dict[str, object]) -> None:
    anchors = report["proof_certificate"]["anchor_results"]
    print("")
    print("Anchor checks:")
    for anchor in anchors:
        status = "ok" if anchor["found"] else "missing"
        lines = ", ".join(str(line) for line in anchor["matched_lines"]) or "-"
        print(f"  {status}: {anchor['id']} ({anchor['file']} lines {lines})")


def print_soft_hits(report: dict[str, object], limit: int = 24) -> None:
    hits = report["proof_certificate"]["soft_phrase_review_hits"]
    print("")
    print("Challenge/extension phrase hits without same-line ledger macro:")
    if not hits:
        print("  none")
        return
    for hit in hits[:limit]:
        print(
            f"  {hit['file']}:{hit['line']}: "
            f"{hit['phrase_group']} -> {hit['matched_text']}"
        )
    if len(hits) > limit:
        print(f"  ... {len(hits) - limit} more; use --format json for full output")


def print_text(report: dict[str, object]) -> None:
    result = report["result"]
    print("Field ledger vocabulary audit")
    print(f"Proof status: {report['proof_status']}")
    print(f"Theorem/problem ID: {report['theorem_or_problem_id']}")
    print("Input params:")
    for source in report["input_parameters"]["source_files"]:
        print(f"  source_file={source}")
    print("Exact object: line-based field-ledger vocabulary scan; random_seed=None")
    print("")
    print("Macro counts by file:")
    for file_name, counts in result["macro_counts_by_file"].items():
        rendered = ", ".join(f"{macro}={count}" for macro, count in counts.items())
        print(f"  {file_name}: {rendered}")
    print("")
    print("Phrase counts:")
    for phrase_group, count in result["phrase_counts_by_group"].items():
        print(f"  {phrase_group}: {count}")
    print("")
    print("Macro definitions:")
    for macro, locations in result["macro_definitions"].items():
        rendered = ", ".join(locations) if locations else "none"
        print(f"  {macro}: {rendered}")
    print_anchor_results(report)
    print_soft_hits(report)
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
