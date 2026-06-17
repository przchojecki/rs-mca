#!/usr/bin/env python3
"""Inventory the TeX/PDF release bundle.

Proof status: AUDIT. This script checks release hygiene metadata for the stable
paper bundle. It does not compile TeX, inspect PDF internals, or modify stable
sources; it records source/PDF pairing, content hashes, titles, and date
declarations for review.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
TEX_DIR = REPO_ROOT / "tex"

THEOREM_PROBLEM_ID = "stable-tex-pdf-release-bundle-inventory"
PROOF_STATUS = "AUDIT"
DETERMINISM = "deterministic file-content scan; no random seed"

TITLE_RE = re.compile(r"\\title\s*\{")
DATE_RE = re.compile(r"\\date\s*\{")


@dataclass(frozen=True)
class BundleEntry:
    stem: str
    tex_file: str | None
    pdf_file: str | None
    tex_sha256: str | None
    pdf_sha256: str | None
    tex_bytes: int | None
    pdf_bytes: int | None
    title: str | None
    date: str | None
    dynamic_date: bool
    review_reasons: list[str]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def strip_tex_comments(text: str) -> str:
    cleaned_lines: list[str] = []
    for line in text.splitlines():
        cleaned_lines.append(strip_tex_comment(line))
    return "\n".join(cleaned_lines)


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


def extract_command_argument(pattern: re.Pattern[str], text: str) -> str | None:
    match = pattern.search(text)
    if not match:
        return None
    opening_index = match.end() - 1
    closing_index = find_matching_brace(text, opening_index)
    if closing_index is None:
        return None
    return text[opening_index + 1 : closing_index]


def tex_metadata(path: Path | None) -> tuple[str | None, str | None, bool]:
    if path is None:
        return None, None, False
    text = strip_tex_comments(path.read_text(encoding="utf-8"))
    title = normalise_whitespace(extract_command_argument(TITLE_RE, text))
    date = normalise_whitespace(extract_command_argument(DATE_RE, text))
    dynamic_date = date == r"\today"
    return title, date, dynamic_date


def relative(path: Path | None) -> str | None:
    if path is None:
        return None
    return path.relative_to(REPO_ROOT).as_posix()


def collect_bundle_entries() -> list[BundleEntry]:
    tex_files = {path.stem: path for path in sorted(TEX_DIR.glob("*.tex"))}
    pdf_files = {path.stem: path for path in sorted(REPO_ROOT.glob("*.pdf"))}
    stems = sorted(set(tex_files) | set(pdf_files))
    entries: list[BundleEntry] = []

    for stem in stems:
        tex_path = tex_files.get(stem)
        pdf_path = pdf_files.get(stem)
        title, date, dynamic_date = tex_metadata(tex_path)
        review_reasons: list[str] = []
        if tex_path is None:
            review_reasons.append("root PDF has no matching tex source")
        if pdf_path is None:
            review_reasons.append("tex source has no matching root PDF")
        if tex_path is not None and not title:
            review_reasons.append("tex source has no title declaration")
        if tex_path is not None and not date:
            review_reasons.append("tex source has no date declaration")
        if dynamic_date:
            review_reasons.append("tex source uses dynamic \\date{\\today}")

        entries.append(
            BundleEntry(
                stem=stem,
                tex_file=relative(tex_path),
                pdf_file=relative(pdf_path),
                tex_sha256=sha256_file(tex_path) if tex_path else None,
                pdf_sha256=sha256_file(pdf_path) if pdf_path else None,
                tex_bytes=tex_path.stat().st_size if tex_path else None,
                pdf_bytes=pdf_path.stat().st_size if pdf_path else None,
                title=title,
                date=date,
                dynamic_date=dynamic_date,
                review_reasons=review_reasons,
            )
        )

    return entries


def build_report(entries: list[BundleEntry]) -> dict[str, Any]:
    complete_pairs = [
        entry for entry in entries if entry.tex_file and entry.pdf_file
    ]
    missing_tex = [entry for entry in entries if not entry.tex_file]
    missing_pdf = [entry for entry in entries if not entry.pdf_file]
    dynamic_dates = [entry for entry in entries if entry.dynamic_date]
    review_entries = [entry for entry in entries if entry.review_reasons]
    audit_result = "PASS" if not review_entries else "REVIEW"

    return {
        "metadata": {
            "proof_status": PROOF_STATUS,
            "theorem_problem_id": THEOREM_PROBLEM_ID,
            "determinism": DETERMINISM,
            "tex_glob": "tex/*.tex",
            "pdf_glob": "*.pdf",
        },
        "result": {
            "audit_result": audit_result,
            "bundle_entries": len(entries),
            "complete_pairs": len(complete_pairs),
            "missing_tex": len(missing_tex),
            "missing_pdf": len(missing_pdf),
            "dynamic_dates": len(dynamic_dates),
            "entries_requiring_review": len(review_entries),
        },
        "entries_requiring_review": [asdict(entry) for entry in review_entries],
        "entries": [asdict(entry) for entry in entries],
    }


def short_hash(value: str | None) -> str:
    return value[:12] if value else "<none>"


def format_optional(value: str | int | None) -> str:
    if value is None:
        return "<none>"
    return str(value)


def format_text(report: dict[str, Any]) -> str:
    metadata = report["metadata"]
    result = report["result"]
    lines: list[str] = [
        "Release bundle inventory",
        f"proof_status: {metadata['proof_status']}",
        f"theorem_problem_id: {metadata['theorem_problem_id']}",
        f"determinism: {metadata['determinism']}",
        f"tex_glob: {metadata['tex_glob']}",
        f"pdf_glob: {metadata['pdf_glob']}",
        f"audit_result: {result['audit_result']}",
        f"bundle_entries: {result['bundle_entries']}",
        f"complete_pairs: {result['complete_pairs']}",
        f"missing_tex: {result['missing_tex']}",
        f"missing_pdf: {result['missing_pdf']}",
        f"dynamic_dates: {result['dynamic_dates']}",
        f"entries_requiring_review: {result['entries_requiring_review']}",
        "entries:",
    ]

    if not report["entries"]:
        lines.append("  - <none>")
    for entry in report["entries"]:
        reasons = "; ".join(entry["review_reasons"]) or "<none>"
        lines.append(f"  - {entry['stem']}")
        lines.append(
            "    files: "
            f"tex={format_optional(entry['tex_file'])}, "
            f"pdf={format_optional(entry['pdf_file'])}"
        )
        lines.append(
            "    bytes: "
            f"tex={format_optional(entry['tex_bytes'])}, "
            f"pdf={format_optional(entry['pdf_bytes'])}"
        )
        lines.append(
            "    sha256: "
            f"tex={short_hash(entry['tex_sha256'])}, "
            f"pdf={short_hash(entry['pdf_sha256'])}"
        )
        lines.append(
            "    metadata: "
            f"date={format_optional(entry['date'])}, "
            f"title={format_optional(entry['title'])}"
        )
        lines.append(f"    review_reasons: {reasons}")

    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inventory root PDFs and stable TeX sources."
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
    report = build_report(collect_bundle_entries())
    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(format_text(report))


if __name__ == "__main__":
    main()
