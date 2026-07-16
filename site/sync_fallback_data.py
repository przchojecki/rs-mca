#!/usr/bin/env python3
"""Check or refresh the JSON fallbacks embedded in site/index.html.

The site normally fetches the canonical files under site/data.  When that
fetch fails (for example, when the page is opened directly from disk), the
embedded JavaScript values are the public board.  Keeping two hand-edited
copies allowed those offline values to drift.  This script makes the JSON
files authoritative and compares the parsed values, not their formatting.

Run without arguments as a fail-closed drift check.  Pass --write to
replace all three board values with canonical, deterministically formatted
JSON, then verify the result.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SITE_DIR = Path(__file__).resolve().parent
INDEX_PATH = SITE_DIR / "index.html"

FALLBACK_SOURCES = (
    ("fallbackEntriesRaw", SITE_DIR / "data" / "frontier.json"),
    ("fallbackUpdatesRaw", SITE_DIR / "data" / "updates.json"),
    ("fallbackRateBoardsRaw", SITE_DIR / "data" / "rate-leaderboards.json"),
)


@dataclass(frozen=True)
class EmbeddedValue:
    start: int
    end: int
    value: Any | None
    parse_error: str | None


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def balanced_value_end(source: str, start: int) -> int:
    """Return the end of one JavaScript object or array literal."""

    if start >= len(source) or source[start] not in "[{":
        raise ValueError(f"{INDEX_PATH}: fallback value has no opening bracket")

    matching = {"[": "]", "{": "}"}
    stack: list[str] = []
    quote: str | None = None
    escaped = False

    for offset, char in enumerate(source[start:], start=start):
        if quote is not None:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            continue

        if char in ("'", '"'):
            quote = char
        elif char in matching:
            stack.append(matching[char])
        elif char in ("]", "}"):
            if not stack or char != stack.pop():
                raise ValueError(
                    f"{INDEX_PATH}: unbalanced fallback value at {offset}"
                )
            if not stack:
                return offset + 1

    raise ValueError(f"{INDEX_PATH}: unterminated fallback value")


def locate_embedded_value(source: str, variable: str) -> EmbeddedValue:
    anchor = f"const {variable} = "
    count = source.count(anchor)
    if count != 1:
        raise ValueError(
            f"{INDEX_PATH}: expected one {variable!r} declaration, found {count}"
        )

    start = source.index(anchor) + len(anchor)
    end = balanced_value_end(source, start)
    try:
        value = json.loads(source[start:end])
    except json.JSONDecodeError as error:
        value = None
        parse_error = str(error)
    else:
        parse_error = None

    if not source[end:].startswith(";"):
        raise ValueError(
            f"{INDEX_PATH}: {variable} JSON value is not followed by a semicolon"
        )
    return EmbeddedValue(start=start, end=end, value=value, parse_error=parse_error)


def render_embedded_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=4)


def item_count(value: Any) -> str:
    if isinstance(value, list):
        return f"{len(value)} list items"
    if isinstance(value, dict):
        rates = value.get("rates")
        if isinstance(rates, list):
            rows = sum(
                len(rate.get("rows", []))
                for rate in rates
                if isinstance(rate, dict)
            )
            return f"{len(rates)} rates / {rows} rows"
        return f"{len(value)} object keys"
    return type(value).__name__


def first_id_difference(left: Any, right: Any) -> str | None:
    if not isinstance(left, list) or not isinstance(right, list):
        return None
    left_ids = [item.get("id") for item in left if isinstance(item, dict)]
    right_ids = [item.get("id") for item in right if isinstance(item, dict)]
    if not left_ids and not right_ids:
        return None
    if left_ids == right_ids:
        return None
    for index, pair in enumerate(zip(left_ids, right_ids)):
        if pair[0] != pair[1]:
            return f"first differing id at {index}: embedded={pair[0]!r}, canonical={pair[1]!r}"
    return f"id counts differ: embedded={len(left_ids)}, canonical={len(right_ids)}"


def check_source(source: str) -> list[str]:
    failures: list[str] = []
    for variable, canonical_path in FALLBACK_SOURCES:
        embedded_value = locate_embedded_value(source, variable)
        if embedded_value.parse_error is not None:
            failures.append(
                f"{variable} is not strict JSON ({embedded_value.parse_error})"
            )
            continue
        embedded = embedded_value.value
        canonical = load_json(canonical_path)
        if embedded == canonical:
            continue
        detail = first_id_difference(embedded, canonical)
        suffix = f"; {detail}" if detail else ""
        failures.append(
            f"{variable} drifts from {canonical_path.relative_to(SITE_DIR)} "
            f"(embedded {item_count(embedded)}, canonical {item_count(canonical)})"
            f"{suffix}"
        )
    return failures


def refreshed_source(source: str) -> str:
    refreshed = source
    for variable, canonical_path in FALLBACK_SOURCES:
        embedded = locate_embedded_value(refreshed, variable)
        replacement = render_embedded_json(load_json(canonical_path))
        refreshed = refreshed[: embedded.start] + replacement + refreshed[embedded.end :]
    return refreshed


def replace_embedded_value(source: str, variable: str, value: Any) -> str:
    embedded = locate_embedded_value(source, variable)
    replacement = render_embedded_json(value)
    return source[: embedded.start] + replacement + source[embedded.end :]


def expect_rejected(label: str, source: str) -> None:
    try:
        failures = check_source(source)
    except ValueError:
        return
    if failures:
        return
    raise AssertionError(f"tamper was accepted: {label}")


def run_self_test(source: str) -> None:
    clean = refreshed_source(source)
    if failures := check_source(clean):
        raise AssertionError(f"clean synchronization failed: {failures}")

    frontier = load_json(SITE_DIR / "data" / "frontier.json")
    frontier.pop()
    expect_rejected(
        "missing frontier row",
        replace_embedded_value(clean, "fallbackEntriesRaw", frontier),
    )

    updates = load_json(SITE_DIR / "data" / "updates.json")
    updates[0], updates[1] = updates[1], updates[0]
    expect_rejected(
        "update order",
        replace_embedded_value(clean, "fallbackUpdatesRaw", updates),
    )

    rate_boards = load_json(SITE_DIR / "data" / "rate-leaderboards.json")
    kb_row = next(
        row
        for rate in rate_boards["rates"]
        for row in rate["rows"]
        if row.get("id") == "cap25-v13-identity-kb-mca-edge"
    )
    kb_row["agreementA"] = "tampered"
    expect_rejected(
        "nested KoalaBear field",
        replace_embedded_value(clean, "fallbackRateBoardsRaw", rate_boards),
    )

    anchor = "const fallbackEntriesRaw = "
    duplicate = clean.replace(anchor, f"{anchor}[];\n    {anchor}", 1)
    expect_rejected("duplicate declaration", duplicate)

    embedded = locate_embedded_value(clean, "fallbackEntriesRaw")
    truncated = clean[: embedded.end - 1] + clean[embedded.end :]
    expect_rejected("truncated literal", truncated)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument(
        "--write",
        action="store_true",
        help="refresh embedded fallbacks from site/data before checking",
    )
    actions.add_argument(
        "--self-test",
        action="store_true",
        help="run in-memory mutation tests without changing the checkout",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source = INDEX_PATH.read_text(encoding="utf-8")

    if args.self_test:
        run_self_test(source)
        print("site fallback synchronization self-test passed")
        return 0

    if args.write:
        refreshed = refreshed_source(source)
        if refreshed != source:
            INDEX_PATH.write_text(refreshed, encoding="utf-8")
            source = refreshed
            print(f"updated {INDEX_PATH.relative_to(SITE_DIR.parent)}")
        else:
            print("fallback data already current")

    failures = check_source(source)
    if failures:
        for failure in failures:
            print(f"DRIFT: {failure}", file=sys.stderr)
        print("run: python3 site/sync_fallback_data.py --write", file=sys.stderr)
        return 1

    print("site fallback data matches all canonical JSON files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
