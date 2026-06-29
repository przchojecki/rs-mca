#!/usr/bin/env python3
"""Compare the README script-layer manifest with the actual scripts.

Proof status: AUDIT. This deterministic scanner parses the intended
`scripts/` block in `readme.md` and reports which planned scripts currently
exist in the repository. It does not modify the script layer.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
README_PATH = REPO_ROOT / "readme.md"
SCRIPTS_DIR = REPO_ROOT / "scripts"

THEOREM_PROBLEM_ID = "readme-script-layer-manifest-inventory"
PROOF_STATUS = "AUDIT"
DETERMINISM = "deterministic source scan; no random seed"

MANIFEST_INTRO = "The broader intended script layer is:"
SCRIPT_LINE_RE = re.compile(
    r"^\s*(?P<name>[A-Za-z0-9_.-]+\.py)\s*#\s*(?P<description>.+?)\s*$"
)
STATUS_WORDS = (
    "PROVED",
    "CONDITIONAL",
    "CONJECTURAL",
    "EXPERIMENTAL",
    "AUDIT",
    "COUNTEREXAMPLE",
)


@dataclass(frozen=True)
class ManifestEntry:
    path: str
    description: str
    exists: bool
    status_words: list[str]
    sha256: str | None
    bytes: int | None


@dataclass(frozen=True)
class ActualScript:
    path: str
    listed_in_readme: bool
    sha256: str
    bytes: int


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def relative(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def extract_manifest_block(readme_text: str) -> list[str]:
    lines = readme_text.splitlines()
    try:
        intro_index = lines.index(MANIFEST_INTRO)
    except ValueError as exc:
        raise ValueError(f"Could not find README marker: {MANIFEST_INTRO}") from exc

    fence_start: int | None = None
    for index in range(intro_index + 1, len(lines)):
        if lines[index].startswith("```"):
            fence_start = index
            break
    if fence_start is None:
        raise ValueError("Could not find opening manifest fence")

    for index in range(fence_start + 1, len(lines)):
        if lines[index].startswith("```"):
            return lines[fence_start + 1 : index]
    raise ValueError("Could not find closing manifest fence")


def status_words(description: str) -> list[str]:
    upper_description = description.upper()
    return [word for word in STATUS_WORDS if word in upper_description]


def parse_manifest_entries(block_lines: list[str]) -> list[tuple[str, str]]:
    entries: list[tuple[str, str]] = []
    for line in block_lines:
        match = SCRIPT_LINE_RE.match(line)
        if not match:
            continue
        entries.append(
            (
                f"scripts/{match.group('name')}",
                match.group("description"),
            )
        )
    return entries


def actual_scripts() -> dict[str, Path]:
    if not SCRIPTS_DIR.exists():
        return {}
    return {
        relative(path): path
        for path in sorted(SCRIPTS_DIR.glob("*.py"))
    }


def build_report() -> dict[str, Any]:
    readme_text = README_PATH.read_text(encoding="utf-8")
    manifest_pairs = parse_manifest_entries(extract_manifest_block(readme_text))
    actual = actual_scripts()
    manifest_paths = {path for path, _description in manifest_pairs}

    manifest_entries: list[ManifestEntry] = []
    for path, description in manifest_pairs:
        actual_path = actual.get(path)
        manifest_entries.append(
            ManifestEntry(
                path=path,
                description=description,
                exists=actual_path is not None,
                status_words=status_words(description),
                sha256=sha256_file(actual_path) if actual_path else None,
                bytes=actual_path.stat().st_size if actual_path else None,
            )
        )

    actual_entries = [
        ActualScript(
            path=path,
            listed_in_readme=path in manifest_paths,
            sha256=sha256_file(actual_path),
            bytes=actual_path.stat().st_size,
        )
        for path, actual_path in actual.items()
    ]
    missing_from_repo = [entry for entry in manifest_entries if not entry.exists]
    unlisted_actual = [
        entry for entry in actual_entries if not entry.listed_in_readme
    ]
    listed_actual = [
        entry for entry in actual_entries if entry.listed_in_readme
    ]
    audit_result = "PASS"
    if missing_from_repo or unlisted_actual:
        audit_result = "REVIEW"

    return {
        "metadata": {
            "proof_status": PROOF_STATUS,
            "theorem_problem_id": THEOREM_PROBLEM_ID,
            "determinism": DETERMINISM,
            "readme": relative(README_PATH),
            "manifest_marker": MANIFEST_INTRO,
            "scripts_glob": "scripts/*.py",
        },
        "result": {
            "audit_result": audit_result,
            "manifest_entries": len(manifest_entries),
            "actual_scripts": len(actual_entries),
            "listed_actual_scripts": len(listed_actual),
            "missing_from_repo": len(missing_from_repo),
            "unlisted_actual_scripts": len(unlisted_actual),
        },
        "missing_from_repo": [asdict(entry) for entry in missing_from_repo],
        "unlisted_actual_scripts": [
            asdict(entry) for entry in unlisted_actual
        ],
        "manifest_entries": [asdict(entry) for entry in manifest_entries],
        "actual_scripts": [asdict(entry) for entry in actual_entries],
    }


def short_hash(value: str | None) -> str:
    return value[:12] if value else "<none>"


def format_text(report: dict[str, Any]) -> str:
    metadata = report["metadata"]
    result = report["result"]
    lines: list[str] = [
        "README script-layer inventory",
        f"proof_status: {metadata['proof_status']}",
        f"theorem_problem_id: {metadata['theorem_problem_id']}",
        f"determinism: {metadata['determinism']}",
        f"readme: {metadata['readme']}",
        f"manifest_marker: {metadata['manifest_marker']}",
        f"scripts_glob: {metadata['scripts_glob']}",
        f"audit_result: {result['audit_result']}",
        f"manifest_entries: {result['manifest_entries']}",
        f"actual_scripts: {result['actual_scripts']}",
        f"listed_actual_scripts: {result['listed_actual_scripts']}",
        f"missing_from_repo: {result['missing_from_repo']}",
        f"unlisted_actual_scripts: {result['unlisted_actual_scripts']}",
        "manifest_entries:",
    ]

    for entry in report["manifest_entries"]:
        status = ",".join(entry["status_words"]) or "<none>"
        lines.append(
            "  - "
            f"{entry['path']} exists={entry['exists']} "
            f"status={status} sha256={short_hash(entry['sha256'])}"
        )
        lines.append(f"    description: {entry['description']}")

    lines.append("unlisted_actual_scripts:")
    if not report["unlisted_actual_scripts"]:
        lines.append("  - <none>")
    else:
        for entry in report["unlisted_actual_scripts"]:
            lines.append(
                "  - "
                f"{entry['path']} bytes={entry['bytes']} "
                f"sha256={short_hash(entry['sha256'])}"
            )

    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare README intended scripts with actual scripts."
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
    report = build_report()
    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(format_text(report))


if __name__ == "__main__":
    main()
