#!/usr/bin/env python3
"""Audit reproducibility metadata for repository scripts.

Proof status: AUDIT. This is a deterministic source-level scanner, not a
mathematical proof. It checks whether scripts expose enough metadata to support
the repository convention that computational contributions report inputs,
outputs, certificates or seeds, theorem/problem identifiers, and proof status.
"""

from __future__ import annotations

import argparse
import ast
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_GLOB = "scripts/*.py"

THEOREM_PROBLEM_ID = "scripts-reproducibility-metadata-audit"
PROOF_STATUS = "AUDIT"
DETERMINISM = "deterministic source scan; no random seed"

STATUS_WORDS = (
    "PROVED",
    "CONDITIONAL",
    "CONJECTURAL",
    "EXPERIMENTAL",
    "AUDIT",
    "COUNTEREXAMPLE",
)

REPRODUCIBILITY_MARKERS = (
    "proof_status",
    "theorem_problem_id",
    "certificate",
    "seed",
    "json",
)


@dataclass(frozen=True)
class FileWrite:
    line: int
    target: str
    mode: str
    relative_path: bool


@dataclass(frozen=True)
class ScriptAudit:
    file: str
    line_count: int
    imports: list[str]
    third_party_imports: list[str]
    has_main_guard: bool
    uses_argparse: bool
    uses_sys_argv: bool
    print_calls: int
    file_writes: list[FileWrite]
    has_status_word: bool
    has_reproducibility_marker: bool
    has_json_marker: bool
    review_reasons: list[str]


def is_stdlib_module(module_name: str) -> bool:
    top_level = module_name.split(".", 1)[0]
    stdlib_names = getattr(sys, "stdlib_module_names", None)
    if stdlib_names is None:
        return top_level in {
            "argparse",
            "ast",
            "collections",
            "dataclasses",
            "itertools",
            "json",
            "math",
            "pathlib",
            "sys",
            "time",
            "typing",
        }
    return top_level in stdlib_names


def literal_text(node: ast.AST) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr):
        return "<f-string>"
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = literal_text(node.value)
        if parent:
            return f"{parent}.{node.attr}"
        return node.attr
    return None


def is_main_guard(node: ast.If) -> bool:
    test = node.test
    if not isinstance(test, ast.Compare) or len(test.ops) != 1:
        return False
    if not isinstance(test.ops[0], ast.Eq) or len(test.comparators) != 1:
        return False

    left = literal_text(test.left)
    right = literal_text(test.comparators[0])
    return {left, right} == {"__name__", "__main__"}


def call_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = call_name(node.value)
        if parent:
            return f"{parent}.{node.attr}"
        return node.attr
    return None


def open_call_write(call: ast.Call) -> FileWrite | None:
    function = call_name(call.func)
    if function not in {"open", "Path.open", "pathlib.Path.open"}:
        return None

    target = "<unknown>"
    mode = "r"
    if call.args:
        target = literal_text(call.args[0]) or "<dynamic>"
    if len(call.args) >= 2:
        mode = literal_text(call.args[1]) or "<dynamic>"
    for keyword in call.keywords:
        if keyword.arg == "mode":
            mode = literal_text(keyword.value) or "<dynamic>"

    if not any(flag in mode for flag in ("w", "a", "x", "+")):
        return None

    relative_path = False
    if target not in {"<dynamic>", "<unknown>", "<f-string>"}:
        relative_path = not Path(target).is_absolute()

    return FileWrite(
        line=getattr(call, "lineno", 0),
        target=target,
        mode=mode,
        relative_path=relative_path,
    )


def import_names(tree: ast.AST) -> list[str]:
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)
    return sorted(set(imports))


def audit_script(relative_path: str) -> ScriptAudit:
    path = REPO_ROOT / relative_path
    text = path.read_text(encoding="utf-8")
    tree = ast.parse(text, filename=relative_path)
    lower_text = text.lower()

    imports = import_names(tree)
    third_party_imports = [
        module
        for module in imports
        if not is_stdlib_module(module)
        and not module.startswith(("scripts", "experimental"))
    ]

    has_main_guard = any(
        isinstance(node, ast.If) and is_main_guard(node)
        for node in ast.walk(tree)
    )
    uses_argparse = "argparse" in imports or "argparse" in lower_text
    uses_sys_argv = "sys.argv" in text
    print_calls = sum(
        1
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and call_name(node.func) == "print"
    )
    file_writes = [
        write
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        for write in [open_call_write(node)]
        if write is not None
    ]
    has_status_word = any(word.lower() in lower_text for word in STATUS_WORDS)
    has_reproducibility_marker = any(
        marker in lower_text for marker in REPRODUCIBILITY_MARKERS
    )
    has_json_marker = "json" in lower_text

    review_reasons: list[str] = []
    if not has_main_guard:
        review_reasons.append("missing __main__ guard")
    if uses_sys_argv and not uses_argparse:
        review_reasons.append("uses sys.argv without argparse")
    if not has_status_word:
        review_reasons.append("missing explicit proof-status word")
    if not has_reproducibility_marker:
        review_reasons.append("missing reproducibility marker")
    if not has_json_marker:
        review_reasons.append("missing JSON output marker")
    if any(write.relative_path for write in file_writes):
        review_reasons.append("writes to a relative output path")

    return ScriptAudit(
        file=relative_path,
        line_count=len(text.splitlines()),
        imports=imports,
        third_party_imports=third_party_imports,
        has_main_guard=has_main_guard,
        uses_argparse=uses_argparse,
        uses_sys_argv=uses_sys_argv,
        print_calls=print_calls,
        file_writes=file_writes,
        has_status_word=has_status_word,
        has_reproducibility_marker=has_reproducibility_marker,
        has_json_marker=has_json_marker,
        review_reasons=review_reasons,
    )


def collect_scripts() -> list[str]:
    return [
        path.relative_to(REPO_ROOT).as_posix()
        for path in sorted(REPO_ROOT.glob(SCRIPT_GLOB))
    ]


def build_report(audits: list[ScriptAudit]) -> dict[str, Any]:
    scripts_requiring_review = [
        audit for audit in audits if audit.review_reasons
    ]
    third_party_imports = sorted(
        {
            module
            for audit in audits
            for module in audit.third_party_imports
        }
    )
    file_write_count = sum(len(audit.file_writes) for audit in audits)
    relative_write_count = sum(
        1
        for audit in audits
        for write in audit.file_writes
        if write.relative_path
    )
    audit_result = "PASS" if not scripts_requiring_review else "REVIEW"

    return {
        "metadata": {
            "proof_status": PROOF_STATUS,
            "theorem_problem_id": THEOREM_PROBLEM_ID,
            "determinism": DETERMINISM,
            "script_glob": SCRIPT_GLOB,
            "status_words": list(STATUS_WORDS),
            "reproducibility_markers": list(REPRODUCIBILITY_MARKERS),
        },
        "result": {
            "audit_result": audit_result,
            "scripts_checked": len(audits),
            "scripts_requiring_review": len(scripts_requiring_review),
            "third_party_imports": third_party_imports,
            "file_writes": file_write_count,
            "relative_file_writes": relative_write_count,
        },
        "scripts_requiring_review": [
            asdict(audit) for audit in scripts_requiring_review
        ],
        "scripts": [asdict(audit) for audit in audits],
    }


def format_bool(value: bool) -> str:
    return "yes" if value else "no"


def format_text(report: dict[str, Any]) -> str:
    metadata = report["metadata"]
    result = report["result"]
    lines: list[str] = [
        "Script reproducibility audit",
        f"proof_status: {metadata['proof_status']}",
        f"theorem_problem_id: {metadata['theorem_problem_id']}",
        f"determinism: {metadata['determinism']}",
        f"script_glob: {metadata['script_glob']}",
        f"audit_result: {result['audit_result']}",
        f"scripts_checked: {result['scripts_checked']}",
        f"scripts_requiring_review: {result['scripts_requiring_review']}",
        "third_party_imports: "
        + (", ".join(result["third_party_imports"]) or "<none>"),
        f"file_writes: {result['file_writes']}",
        f"relative_file_writes: {result['relative_file_writes']}",
        "scripts:",
    ]

    if not report["scripts"]:
        lines.append("  - <none>")
    for audit in report["scripts"]:
        reasons = "; ".join(audit["review_reasons"]) or "<none>"
        writes = ", ".join(
            f"{write['target']} mode={write['mode']} line={write['line']}"
            for write in audit["file_writes"]
        ) or "<none>"
        lines.append(f"  - {audit['file']}")
        lines.append(f"    review_reasons: {reasons}")
        lines.append(
            "    cli: "
            f"main_guard={format_bool(audit['has_main_guard'])}, "
            f"argparse={format_bool(audit['uses_argparse'])}, "
            f"sys_argv={format_bool(audit['uses_sys_argv'])}"
        )
        lines.append(
            "    metadata: "
            f"status_word={format_bool(audit['has_status_word'])}, "
            "reproducibility_marker="
            f"{format_bool(audit['has_reproducibility_marker'])}, "
            f"json_marker={format_bool(audit['has_json_marker'])}"
        )
        third_party = ", ".join(audit["third_party_imports"]) or "<none>"
        lines.append(f"    third_party_imports: {third_party}")
        lines.append(f"    file_writes: {writes}")

    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit reproducibility metadata for repository scripts."
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
    audits = [audit_script(path) for path in collect_scripts()]
    report = build_report(audits)
    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(format_text(report))


if __name__ == "__main__":
    main()
