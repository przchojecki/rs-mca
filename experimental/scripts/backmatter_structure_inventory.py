#!/usr/bin/env python3
"""Inventory appendix and bibliography backmatter structure in stable TeX.

Proof status: AUDIT. This deterministic scanner records appendix markers,
appendix headings, bibliography environments, bibitems, and end-document
markers. It checks ordering and closure but does not validate citations or
reference targets.
"""

from __future__ import annotations

import argparse
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

THEOREM_PROBLEM_ID = "stable-tex-backmatter-structure-inventory"
PROOF_STATUS = "AUDIT"
DETERMINISM = "deterministic source scan; no random seed"

APPENDIX_RE = re.compile(r"\\appendix(?![A-Za-z])")
BIB_BEGIN_RE = re.compile(
    r"\\begin\{thebibliography\}(?:\{(?P<argument>[^{}]*)\})?"
)
BIB_END_RE = re.compile(r"\\end\{thebibliography\}")
BIBITEM_RE = re.compile(r"\\bibitem(?:\[[^\]]*\])?\{(?P<key>[^{}]+)\}")
END_DOCUMENT_RE = re.compile(r"\\end\{document\}")
HEADING_RE = re.compile(
    r"\\(?P<command>part|section|subsection|subsubsection)"
    r"(?P<star>\*)?\s*\{(?P<title>[^{}]+)\}"
)


@dataclass(frozen=True)
class LineEntry:
    file: str
    line: int
    value: str | None = None


@dataclass(frozen=True)
class BibitemEntry:
    file: str
    line: int
    key: str
    in_bibliography: bool


@dataclass(frozen=True)
class HeadingEntry:
    file: str
    line: int
    command: str
    starred: bool
    title: str


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


def read_stripped_lines(relative_path: str) -> list[str]:
    path = REPO_ROOT / relative_path
    return [
        strip_tex_comment(line)
        for line in path.read_text(encoding="utf-8").splitlines()
    ]


def normalise_text(value: str) -> str:
    return " ".join(value.split())


def scan_file(relative_path: str) -> dict[str, Any]:
    lines = read_stripped_lines(relative_path)
    appendices: list[LineEntry] = []
    bibliography_begins: list[LineEntry] = []
    bibliography_ends: list[LineEntry] = []
    bibitems: list[BibitemEntry] = []
    end_documents: list[LineEntry] = []
    appendix_headings: list[HeadingEntry] = []
    content_after_end_document: list[LineEntry] = []

    in_bibliography = False
    first_appendix_line: int | None = None
    first_bibliography_line: int | None = None
    first_end_document_line: int | None = None

    for line_number, line in enumerate(lines, start=1):
        stripped = line.strip()

        if first_end_document_line is not None and stripped:
            content_after_end_document.append(
                LineEntry(
                    file=relative_path,
                    line=line_number,
                    value=normalise_text(stripped),
                )
            )

        for match in APPENDIX_RE.finditer(line):
            appendices.append(LineEntry(file=relative_path, line=line_number))
            if first_appendix_line is None:
                first_appendix_line = line_number

        for match in BIB_BEGIN_RE.finditer(line):
            argument = match.group("argument")
            bibliography_begins.append(
                LineEntry(
                    file=relative_path,
                    line=line_number,
                    value=argument.strip() if argument else None,
                )
            )
            in_bibliography = True
            if first_bibliography_line is None:
                first_bibliography_line = line_number

        for match in BIBITEM_RE.finditer(line):
            bibitems.append(
                BibitemEntry(
                    file=relative_path,
                    line=line_number,
                    key=match.group("key"),
                    in_bibliography=in_bibliography,
                )
            )

        for match in HEADING_RE.finditer(line):
            if first_appendix_line is None:
                continue
            if first_bibliography_line is not None:
                continue
            if first_end_document_line is not None:
                continue
            appendix_headings.append(
                HeadingEntry(
                    file=relative_path,
                    line=line_number,
                    command=match.group("command"),
                    starred=bool(match.group("star")),
                    title=normalise_text(match.group("title")),
                )
            )

        for match in BIB_END_RE.finditer(line):
            bibliography_ends.append(LineEntry(file=relative_path, line=line_number))
            in_bibliography = False

        for match in END_DOCUMENT_RE.finditer(line):
            end_documents.append(LineEntry(file=relative_path, line=line_number))
            if first_end_document_line is None:
                first_end_document_line = line_number

    return build_file_report(
        relative_path=relative_path,
        appendices=appendices,
        bibliography_begins=bibliography_begins,
        bibliography_ends=bibliography_ends,
        bibitems=bibitems,
        end_documents=end_documents,
        appendix_headings=appendix_headings,
        content_after_end_document=content_after_end_document,
    )


def build_file_report(
    relative_path: str,
    appendices: list[LineEntry],
    bibliography_begins: list[LineEntry],
    bibliography_ends: list[LineEntry],
    bibitems: list[BibitemEntry],
    end_documents: list[LineEntry],
    appendix_headings: list[HeadingEntry],
    content_after_end_document: list[LineEntry],
) -> dict[str, Any]:
    issues: list[str] = []
    if len(end_documents) != 1:
        issues.append("end-document count is not one")
    if len(bibliography_begins) != 1:
        issues.append("bibliography begin count is not one")
    if len(bibliography_ends) != 1:
        issues.append("bibliography end count is not one")

    if bibliography_begins and bibliography_ends:
        if bibliography_begins[0].line > bibliography_ends[0].line:
            issues.append("bibliography end appears before begin")

    if bibliography_begins and end_documents:
        if bibliography_begins[0].line > end_documents[0].line:
            issues.append("bibliography begins after end-document")

    if bibliography_ends and end_documents:
        if bibliography_ends[-1].line > end_documents[0].line:
            issues.append("bibliography ends after end-document")

    for appendix in appendices:
        if bibliography_begins and appendix.line > bibliography_begins[0].line:
            issues.append("appendix marker appears after bibliography")
        if end_documents and appendix.line > end_documents[0].line:
            issues.append("appendix marker appears after end-document")

    if bibliography_begins and bibliography_ends:
        bibitems_inside = [
            item
            for item in bibitems
            if bibliography_begins[0].line < item.line < bibliography_ends[-1].line
        ]
        if not bibitems_inside:
            issues.append("bibliography contains no bibitems")

    if any(not item.in_bibliography for item in bibitems):
        issues.append("bibitem outside bibliography")
    if content_after_end_document:
        issues.append("content after end-document")

    return {
        "file": relative_path,
        "audit_result": "REVIEW" if issues else "PASS",
        "review_items": sorted(set(issues)),
        "appendices": [asdict(entry) for entry in appendices],
        "appendix_headings": [asdict(entry) for entry in appendix_headings],
        "bibliography_begins": [asdict(entry) for entry in bibliography_begins],
        "bibliography_ends": [asdict(entry) for entry in bibliography_ends],
        "bibitems": [asdict(entry) for entry in bibitems],
        "end_documents": [asdict(entry) for entry in end_documents],
        "content_after_end_document": [
            asdict(entry) for entry in content_after_end_document
        ],
        "counts": {
            "appendix_markers": len(appendices),
            "appendix_headings": len(appendix_headings),
            "bibliography_begins": len(bibliography_begins),
            "bibliography_ends": len(bibliography_ends),
            "bibitems": len(bibitems),
            "end_documents": len(end_documents),
            "content_after_end_document": len(content_after_end_document),
        },
    }


def build_report() -> dict[str, Any]:
    file_reports = [scan_file(source) for source in SOURCE_FILES]
    review_files = [
        file_report["file"]
        for file_report in file_reports
        if file_report["audit_result"] == "REVIEW"
    ]
    totals = {
        "appendix_markers": sum(
            file_report["counts"]["appendix_markers"]
            for file_report in file_reports
        ),
        "appendix_headings": sum(
            file_report["counts"]["appendix_headings"]
            for file_report in file_reports
        ),
        "bibliography_environments": sum(
            file_report["counts"]["bibliography_begins"]
            for file_report in file_reports
        ),
        "bibitems": sum(
            file_report["counts"]["bibitems"] for file_report in file_reports
        ),
        "end_documents": sum(
            file_report["counts"]["end_documents"]
            for file_report in file_reports
        ),
        "content_after_end_document": sum(
            file_report["counts"]["content_after_end_document"]
            for file_report in file_reports
        ),
    }

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
            **totals,
        },
        "files": file_reports,
    }


def format_file_summary(file_report: dict[str, Any]) -> str:
    counts = file_report["counts"]
    return (
        f"  - {file_report['file']}: {file_report['audit_result']}; "
        f"appendix_markers={counts['appendix_markers']}, "
        f"appendix_headings={counts['appendix_headings']}, "
        f"bibliographies={counts['bibliography_begins']}, "
        f"bibitems={counts['bibitems']}, "
        f"end_documents={counts['end_documents']}"
    )


def format_text(report: dict[str, Any]) -> str:
    metadata = report["metadata"]
    result = report["result"]
    lines = [
        "Backmatter structure inventory",
        f"Proof status: {metadata['proof_status']}",
        f"Theorem/problem id: {metadata['theorem_problem_id']}",
        f"Determinism: {metadata['determinism']}",
        f"Audit result: {result['audit_result']}",
        "",
        "Summary:",
        f"  files scanned: {result['files_scanned']}",
        f"  review files: {result['review_files']}",
        f"  appendix markers: {result['appendix_markers']}",
        f"  appendix headings: {result['appendix_headings']}",
        f"  bibliography environments: {result['bibliography_environments']}",
        f"  bibitems: {result['bibitems']}",
        f"  end-document markers: {result['end_documents']}",
        "  content lines after end-document: "
        f"{result['content_after_end_document']}",
        "",
        "Per-file backmatter:",
    ]

    for file_report in report["files"]:
        lines.append(format_file_summary(file_report))

    lines.append("")
    lines.append("Review items:")
    review_lines = []
    for file_report in report["files"]:
        if file_report["review_items"]:
            items = ", ".join(file_report["review_items"])
            review_lines.append(f"  - {file_report['file']}: {items}")
    if review_lines:
        lines.extend(review_lines)
    else:
        lines.append("  - none")

    lines.append("")
    lines.append("Appendix headings:")
    headings = [
        heading
        for file_report in report["files"]
        for heading in file_report["appendix_headings"]
    ]
    if headings:
        for heading in headings:
            lines.append(
                f"  - {heading['file']}:{heading['line']} "
                f"\\{heading['command']} title={heading['title']!r}"
            )
    else:
        lines.append("  - none")

    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Inventory appendix, bibliography, bibitem, and end-document "
            "structure across stable TeX manuscripts."
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
