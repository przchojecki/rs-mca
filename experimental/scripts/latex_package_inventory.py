#!/usr/bin/env python3
"""Inventory LaTeX package usage across stable TeX manuscripts.

Proof status: AUDIT. This deterministic scanner records document classes,
package declarations, package option variants, and per-file package sets. It
does not compile or modify stable TeX.
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

THEOREM_PROBLEM_ID = "stable-tex-latex-package-inventory"
PROOF_STATUS = "AUDIT"
DETERMINISM = "deterministic source scan; no random seed"

COMMAND_RE = re.compile(
    r"\\(?P<command>documentclass|usepackage|RequirePackage)"
    r"\s*(?:\[(?P<options>[^\]]*)\])?\s*\{(?P<argument>[^{}]+)\}"
)
PASS_OPTIONS_RE = re.compile(
    r"\\PassOptionsToPackage\s*\{(?P<options>[^{}]+)\}\s*\{(?P<package>[^{}]+)\}"
)


@dataclass(frozen=True)
class DocumentClassEntry:
    file: str
    line: int
    document_class: str
    options: str | None


@dataclass(frozen=True)
class PackageEntry:
    file: str
    line: int
    command: str
    package: str
    options: str | None


@dataclass(frozen=True)
class PassOptionsEntry:
    file: str
    line: int
    package: str
    options: str


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


def normalise_options(value: str | None) -> str | None:
    if value is None:
        return None
    parts = [part.strip() for part in value.split(",") if part.strip()]
    return ",".join(parts) if parts else None


def package_names(argument: str) -> list[str]:
    return [part.strip() for part in argument.split(",") if part.strip()]


def scan_file(
    relative_path: str,
) -> tuple[list[DocumentClassEntry], list[PackageEntry], list[PassOptionsEntry]]:
    path = REPO_ROOT / relative_path
    document_classes: list[DocumentClassEntry] = []
    packages: list[PackageEntry] = []
    pass_options: list[PassOptionsEntry] = []

    for line_number, raw_line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        line = strip_tex_comment(raw_line)
        for pass_match in PASS_OPTIONS_RE.finditer(line):
            pass_options.append(
                PassOptionsEntry(
                    file=relative_path,
                    line=line_number,
                    package=pass_match.group("package").strip(),
                    options=normalise_options(pass_match.group("options")) or "",
                )
            )

        for match in COMMAND_RE.finditer(line):
            command = match.group("command")
            options = normalise_options(match.group("options"))
            names = package_names(match.group("argument"))
            if command == "documentclass":
                for document_class in names:
                    document_classes.append(
                        DocumentClassEntry(
                            file=relative_path,
                            line=line_number,
                            document_class=document_class,
                            options=options,
                        )
                    )
                continue

            for name in names:
                packages.append(
                    PackageEntry(
                        file=relative_path,
                        line=line_number,
                        command=command,
                        package=name,
                        options=options,
                    )
                )

    return document_classes, packages, pass_options


def option_display(value: str | None) -> str:
    return value if value else "<none>"


def build_report(
    document_classes: list[DocumentClassEntry],
    packages: list[PackageEntry],
    pass_options: list[PassOptionsEntry],
) -> dict[str, Any]:
    package_counts = Counter(entry.package for entry in packages)
    package_files: dict[str, set[str]] = defaultdict(set)
    option_variants: dict[str, set[str]] = defaultdict(set)
    packages_by_file: dict[str, list[str]] = {source: [] for source in SOURCE_FILES}

    for entry in packages:
        package_files[entry.package].add(entry.file)
        option_variants[entry.package].add(option_display(entry.options))
        packages_by_file.setdefault(entry.file, []).append(entry.package)

    document_class_variants = Counter(
        (entry.document_class, option_display(entry.options))
        for entry in document_classes
    )
    packages_with_option_drift = {
        package: sorted(options)
        for package, options in sorted(option_variants.items())
        if len(options) > 1
    }
    packages_not_in_all_files = {
        package: sorted(set(SOURCE_FILES) - files)
        for package, files in sorted(package_files.items())
        if len(files) != len(SOURCE_FILES)
    }
    audit_result = "PASS"
    if packages_with_option_drift:
        audit_result = "REVIEW"

    return {
        "metadata": {
            "proof_status": PROOF_STATUS,
            "theorem_problem_id": THEOREM_PROBLEM_ID,
            "determinism": DETERMINISM,
            "input_files": list(SOURCE_FILES),
        },
        "result": {
            "audit_result": audit_result,
            "documentclass_declarations": len(document_classes),
            "package_declarations": len(packages),
            "unique_packages": len(package_counts),
            "pass_options_to_package": len(pass_options),
            "packages_with_option_drift": len(packages_with_option_drift),
            "packages_not_in_all_files": len(packages_not_in_all_files),
        },
        "counts": {
            "packages": dict(sorted(package_counts.items())),
            "documentclass_variants": {
                f"{document_class}[{options}]": count
                for (document_class, options), count in sorted(
                    document_class_variants.items()
                )
            },
            "packages_by_file": {
                source: sorted(set(packages_by_file[source]))
                for source in SOURCE_FILES
            },
        },
        "packages_with_option_drift": packages_with_option_drift,
        "packages_not_in_all_files": packages_not_in_all_files,
        "pass_options_to_package": [asdict(entry) for entry in pass_options],
        "documentclasses": [asdict(entry) for entry in document_classes],
        "packages": [asdict(entry) for entry in packages],
    }


def format_text(report: dict[str, Any]) -> str:
    metadata = report["metadata"]
    result = report["result"]
    counts = report["counts"]
    lines: list[str] = [
        "LaTeX package inventory",
        f"proof_status: {metadata['proof_status']}",
        f"theorem_problem_id: {metadata['theorem_problem_id']}",
        f"determinism: {metadata['determinism']}",
        "input_files:",
    ]
    lines.extend(f"  - {source}" for source in metadata["input_files"])
    lines.extend(
        [
            f"audit_result: {result['audit_result']}",
            f"documentclass_declarations: {result['documentclass_declarations']}",
            f"package_declarations: {result['package_declarations']}",
            f"unique_packages: {result['unique_packages']}",
            f"pass_options_to_package: {result['pass_options_to_package']}",
            "packages_with_option_drift: "
            f"{result['packages_with_option_drift']}",
            f"packages_not_in_all_files: {result['packages_not_in_all_files']}",
            "documentclass_variants:",
        ]
    )
    for variant, count in counts["documentclass_variants"].items():
        lines.append(f"  - {variant}: {count}")

    lines.append("packages:")
    for package, count in counts["packages"].items():
        lines.append(f"  - {package}: {count}")

    lines.append("option_drift:")
    if report["packages_with_option_drift"]:
        for package, options in report["packages_with_option_drift"].items():
            lines.append(f"  - {package}: {', '.join(options)}")
    else:
        lines.append("  - <none>")

    lines.append("packages_by_file:")
    for source, packages in counts["packages_by_file"].items():
        lines.append(f"  - {source}: {', '.join(packages) or '<none>'}")

    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inventory LaTeX package declarations in stable TeX."
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
    all_document_classes: list[DocumentClassEntry] = []
    all_packages: list[PackageEntry] = []
    all_pass_options: list[PassOptionsEntry] = []
    for source in SOURCE_FILES:
        document_classes, packages, pass_options = scan_file(source)
        all_document_classes.extend(document_classes)
        all_packages.extend(packages)
        all_pass_options.extend(pass_options)

    report = build_report(
        all_document_classes,
        all_packages,
        all_pass_options,
    )
    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(format_text(report))


if __name__ == "__main__":
    main()
