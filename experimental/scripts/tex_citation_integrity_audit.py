#!/usr/bin/env python3
"""Audit TeX citation/bibliography integrity in the stable manuscripts.

Proof status: AUDIT.

Each manuscript carries its own bibliography, so this audit checks citation keys
within each file.  It reports cited keys, bibitems, undefined same-file
citations, within-file duplicate bibitems, cross-file duplicate bibkeys, and
unused bibitems.
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
PROBLEM_ID = "Stable-TeX citation integrity audit"


CITE_RE = re.compile(
    r"\\(?P<command>cite[a-zA-Z]*|nocite)\s*"
    r"(?:\[[^\]]*\]\s*)*"
    r"\{(?P<keys>[^}]+)\}"
)
BIBITEM_RE = re.compile(r"\\bibitem(?:\[[^\]]*\])?\{(?P<key>[^}]+)\}")


@dataclass(frozen=True)
class CitationOccurrence:
    file: str
    line: int
    command: str
    key: str
    raw_argument: str
    snippet: str


@dataclass(frozen=True)
class BibitemOccurrence:
    file: str
    line: int
    key: str
    snippet: str


@dataclass(frozen=True)
class UndefinedCitation:
    file: str
    line: int
    command: str
    key: str
    raw_argument: str
    snippet: str


@dataclass(frozen=True)
class DuplicateBibitem:
    file: str
    key: str
    lines: tuple[int, ...]


@dataclass(frozen=True)
class CrossFileDuplicateBibkey:
    key: str
    locations: tuple[str, ...]


@dataclass(frozen=True)
class UnusedBibitem:
    file: str
    line: int
    key: str
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


def read_lines(root: Path, relative_path: str) -> list[str]:
    return (root / relative_path).read_text(encoding="utf-8").splitlines()


def split_keys(raw_argument: str) -> list[str]:
    return [key.strip() for key in raw_argument.split(",") if key.strip()]


def scan_file(
    root: Path,
    relative_path: str,
) -> tuple[list[CitationOccurrence], list[BibitemOccurrence]]:
    citations: list[CitationOccurrence] = []
    bibitems: list[BibitemOccurrence] = []
    for line_no, raw_line in enumerate(read_lines(root, relative_path), start=1):
        line = strip_comment(raw_line)
        snippet = clean_snippet(line)
        for match in CITE_RE.finditer(line):
            command = match.group("command")
            raw_argument = match.group("keys")
            for key in split_keys(raw_argument):
                citations.append(
                    CitationOccurrence(
                        file=relative_path,
                        line=line_no,
                        command=command,
                        key=key,
                        raw_argument=raw_argument,
                        snippet=snippet,
                    )
                )
        for match in BIBITEM_RE.finditer(line):
            bibitems.append(
                BibitemOccurrence(
                    file=relative_path,
                    line=line_no,
                    key=match.group("key").strip(),
                    snippet=snippet,
                )
            )
    return citations, bibitems


def collect_occurrences() -> tuple[list[CitationOccurrence], list[BibitemOccurrence]]:
    root = repo_root()
    citations: list[CitationOccurrence] = []
    bibitems: list[BibitemOccurrence] = []
    for relative_path in TEX_FILES:
        file_citations, file_bibitems = scan_file(root, relative_path)
        citations.extend(file_citations)
        bibitems.extend(file_bibitems)
    return citations, bibitems


def bibitem_sets_by_file(bibitems: list[BibitemOccurrence]) -> dict[str, set[str]]:
    grouped = {file_name: set() for file_name in TEX_FILES}
    for bibitem in bibitems:
        grouped.setdefault(bibitem.file, set()).add(bibitem.key)
    return grouped


def citation_sets_by_file(citations: list[CitationOccurrence]) -> dict[str, set[str]]:
    grouped = {file_name: set() for file_name in TEX_FILES}
    for citation in citations:
        grouped.setdefault(citation.file, set()).add(citation.key)
    return grouped


def undefined_citations(
    citations: list[CitationOccurrence],
    bibitems: list[BibitemOccurrence],
) -> list[UndefinedCitation]:
    bibitem_sets = bibitem_sets_by_file(bibitems)
    missing: list[UndefinedCitation] = []
    for citation in citations:
        if citation.key in bibitem_sets.get(citation.file, set()):
            continue
        missing.append(
            UndefinedCitation(
                file=citation.file,
                line=citation.line,
                command=citation.command,
                key=citation.key,
                raw_argument=citation.raw_argument,
                snippet=citation.snippet,
            )
        )
    return missing


def duplicate_bibitems_by_file(bibitems: list[BibitemOccurrence]) -> list[DuplicateBibitem]:
    grouped: dict[tuple[str, str], list[int]] = {}
    for bibitem in bibitems:
        grouped.setdefault((bibitem.file, bibitem.key), []).append(bibitem.line)
    return [
        DuplicateBibitem(file=file_name, key=key, lines=tuple(lines))
        for (file_name, key), lines in sorted(grouped.items())
        if len(lines) > 1
    ]


def duplicate_bibkeys_cross_file(
    bibitems: list[BibitemOccurrence],
) -> list[CrossFileDuplicateBibkey]:
    grouped: dict[str, list[str]] = {}
    for bibitem in bibitems:
        grouped.setdefault(bibitem.key, []).append(f"{bibitem.file}:{bibitem.line}")
    return [
        CrossFileDuplicateBibkey(key=key, locations=tuple(locations))
        for key, locations in sorted(grouped.items())
        if len({location.split(":", 1)[0] for location in locations}) > 1
    ]


def unused_bibitems(
    citations: list[CitationOccurrence],
    bibitems: list[BibitemOccurrence],
) -> list[UnusedBibitem]:
    citation_sets = citation_sets_by_file(citations)
    unused: list[UnusedBibitem] = []
    for bibitem in bibitems:
        if bibitem.key in citation_sets.get(bibitem.file, set()):
            continue
        unused.append(
            UnusedBibitem(
                file=bibitem.file,
                line=bibitem.line,
                key=bibitem.key,
                snippet=bibitem.snippet,
            )
        )
    return unused


def count_by_file(
    citations: list[CitationOccurrence],
    bibitems: list[BibitemOccurrence],
    missing: list[UndefinedCitation],
    duplicates: list[DuplicateBibitem],
    unused: list[UnusedBibitem],
) -> dict[str, dict[str, int]]:
    counts: dict[str, dict[str, int]] = {
        file_name: {
            "citations": 0,
            "unique_cited_keys": 0,
            "bibitems": 0,
            "undefined_citations": 0,
            "within_file_duplicate_bibitems": 0,
            "unused_bibitems": 0,
        }
        for file_name in TEX_FILES
    }
    cited_sets = citation_sets_by_file(citations)
    for file_name, cited_keys in cited_sets.items():
        counts[file_name]["unique_cited_keys"] = len(cited_keys)
    for citation in citations:
        counts[citation.file]["citations"] += 1
    for bibitem in bibitems:
        counts[bibitem.file]["bibitems"] += 1
    for item in missing:
        counts[item.file]["undefined_citations"] += 1
    for item in duplicates:
        counts[item.file]["within_file_duplicate_bibitems"] += 1
    for item in unused:
        counts[item.file]["unused_bibitems"] += 1
    return counts


def count_citation_commands(citations: list[CitationOccurrence]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for citation in citations:
        counts[citation.command] = counts.get(citation.command, 0) + 1
    return dict(sorted(counts.items()))


def build_notes(
    missing: list[UndefinedCitation],
    duplicates: list[DuplicateBibitem],
    cross_file_duplicates: list[CrossFileDuplicateBibkey],
    unused: list[UnusedBibitem],
) -> list[str]:
    notes: list[str] = []
    if missing:
        notes.append(f"{len(missing)} same-file citations point to undefined bibitems.")
    if duplicates:
        notes.append(f"{len(duplicates)} bibkeys are duplicated within a manuscript.")
    if cross_file_duplicates:
        notes.append(
            f"{len(cross_file_duplicates)} bibkeys occur in more than one manuscript; "
            "this is informational because each TeX file has its own bibliography."
        )
    if unused:
        notes.append(f"{len(unused)} bibitems are not cited inside their own manuscript.")
    notes.append("This is a syntactic audit only; it does not run LaTeX or BibTeX.")
    return notes


def build_report() -> dict[str, object]:
    citations, bibitems = collect_occurrences()
    missing = undefined_citations(citations, bibitems)
    duplicates = duplicate_bibitems_by_file(bibitems)
    cross_file_duplicates = duplicate_bibkeys_cross_file(bibitems)
    unused = unused_bibitems(citations, bibitems)
    return {
        "proof_status": PROOF_STATUS,
        "theorem_or_problem_id": PROBLEM_ID,
        "input_parameters": {
            "source_files": TEX_FILES,
            "citation_pattern": CITE_RE.pattern,
            "bibitem_pattern": BIBITEM_RE.pattern,
        },
        "exact_object": {
            "audit_type": "line-based same-file TeX citation/bibitem scan",
            "random_seed": None,
        },
        "result": {
            "total_citations": len(citations),
            "total_unique_cited_keys": len({citation.key for citation in citations}),
            "total_bibitems": len(bibitems),
            "undefined_citation_count": len(missing),
            "within_file_duplicate_bibitem_count": len(duplicates),
            "cross_file_duplicate_bibkey_count": len(cross_file_duplicates),
            "unused_bibitem_count": len(unused),
            "citation_command_counts": count_citation_commands(citations),
            "counts_by_file": count_by_file(citations, bibitems, missing, duplicates, unused),
            "notes": build_notes(missing, duplicates, cross_file_duplicates, unused),
        },
        "proof_certificate": {
            "citation_occurrences": [asdict(item) for item in citations],
            "bibitem_occurrences": [asdict(item) for item in bibitems],
            "undefined_citations": [asdict(item) for item in missing],
            "within_file_duplicate_bibitems": [asdict(item) for item in duplicates],
            "cross_file_duplicate_bibkeys": [asdict(item) for item in cross_file_duplicates],
            "unused_bibitems": [asdict(item) for item in unused],
        },
    }


def print_issue_list(title: str, items: list[dict[str, object]], limit: int = 24) -> None:
    print("")
    print(title + ":")
    if not items:
        print("  none")
        return
    for item in items[:limit]:
        if "command" in item:
            print(
                f"  {item['file']}:{item['line']}: "
                f"\\{item['command']}{{{item['raw_argument']}}} -> {item['key']}"
            )
        elif "lines" in item:
            lines = ", ".join(str(line) for line in item["lines"])
            print(f"  {item['file']}: {item['key']} at lines {lines}")
        elif "locations" in item:
            locations = ", ".join(item["locations"])
            print(f"  {item['key']}: {locations}")
        else:
            print(f"  {item['file']}:{item['line']}: {item['key']}")
    if len(items) > limit:
        print(f"  ... {len(items) - limit} more; use --format json for full output")


def print_text(report: dict[str, object]) -> None:
    result = report["result"]
    certificate = report["proof_certificate"]
    print("TeX citation integrity audit")
    print(f"Proof status: {report['proof_status']}")
    print(f"Theorem/problem ID: {report['theorem_or_problem_id']}")
    print("Input params:")
    for source in report["input_parameters"]["source_files"]:
        print(f"  source_file={source}")
    print("Exact object: line-based same-file TeX citation/bibitem scan; random_seed=None")
    print("")
    print("Summary:")
    print(f"  total_citations={result['total_citations']}")
    print(f"  total_unique_cited_keys={result['total_unique_cited_keys']}")
    print(f"  total_bibitems={result['total_bibitems']}")
    print(f"  undefined_citations={result['undefined_citation_count']}")
    print(f"  within_file_duplicate_bibitems={result['within_file_duplicate_bibitem_count']}")
    print(f"  cross_file_duplicate_bibkeys={result['cross_file_duplicate_bibkey_count']}")
    print(f"  unused_bibitems={result['unused_bibitem_count']}")
    print("")
    print("Counts by file:")
    for file_name, counts in result["counts_by_file"].items():
        rendered = ", ".join(f"{name}={count}" for name, count in counts.items())
        print(f"  {file_name}: {rendered}")
    print_issue_list("Undefined same-file citations", certificate["undefined_citations"])
    print_issue_list(
        "Within-file duplicate bibitems",
        certificate["within_file_duplicate_bibitems"],
    )
    print_issue_list("Cross-file duplicate bibkeys", certificate["cross_file_duplicate_bibkeys"])
    print_issue_list("Unused bibitems", certificate["unused_bibitems"])
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
