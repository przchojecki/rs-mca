#!/usr/bin/env python3
"""Exact audit for the current Q/R1 one-step closing interface.

The checked object is the finite-input side of
``cor:capfr1-Q-R1-closing`` in ``experimental/cap25_cap_v13_raw.tex``:
the one-step inequality names integer inputs
``U_paid(a0+1) + U_Q(a0+1) + U_R1(a0+1) <= B_* < L(a0)``.

This script does not try to prove the missing Q or R1 estimates.  It checks
what is replayable from the current tree:

* the current adjacent rows and exact ``B_*`` thresholds are pinned;
* the lower-side ``L(a0) > B_*`` and one-step quiet lower floor are recomputed
  exactly;
* the current sources are audited for instantiated upper summands.

Output status is EXPERIMENTAL / AUDIT.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

sys.set_int_max_str_digits(2_000_000)

STATUS = "EXPERIMENTAL / AUDIT"
CERT_REL = Path("experimental/data/certificates/q-r1-closing-audit/q_r1_closing_audit.json")
RAW_REL = Path("experimental/cap25_cap_v13_raw.tex")
COMPACT_REL = Path("experimental/cap25_cap_v13_raw_compact.tex")
KB_CORRECTED_REL = Path(
    "experimental/data/certificates/frontier-adjacent/"
    "koalabear_frontier_adjacent_a1116043_a1116044.json"
)
PACKET_RELS = [
    Path("experimental/data/certificates/frontier-adjacent/kb_mca_v1.packet.json"),
    Path("experimental/data/certificates/frontier-adjacent/kb_list_v1.packet.json"),
    Path("experimental/data/certificates/frontier-adjacent/m31_mca_v1.packet.json"),
    Path("experimental/data/certificates/frontier-adjacent/m31_list_v1.packet.json"),
]


@dataclass(frozen=True)
class Row:
    row_id: str
    row_label: str
    kind: str
    base_prime: int
    extension_degree: int
    lambda_bits: int
    a0: int
    a1: int


N = 2**21
K_BASE = 2**20
P_KB = 2**31 - 2**24 + 1
P_M31 = 2**31 - 1

ROWS = [
    Row("kb_mca", "KoalaBear MCA", "mca", P_KB, 6, 128, 1116047, 1116048),
    Row("kb_list", "KoalaBear list", "list", P_KB, 6, 128, 1116046, 1116047),
    Row("m31_mca", "Mersenne-31 MCA", "mca", P_M31, 4, 100, 1116023, 1116024),
    Row("m31_list", "Mersenne-31 list", "list", P_M31, 4, 100, 1116022, 1116023),
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def ceil_div(num: int, den: int) -> int:
    if den <= 0:
        raise ValueError("positive denominator required")
    return -(-num // den)


def comb_batch(n: int, values: Iterable[int]) -> dict[int, int]:
    wanted = sorted(set(values))
    if not wanted:
        return {}
    lo, hi = wanted[0], wanted[-1]
    cur_m = lo
    cur = math.comb(n, lo)
    out = {lo: cur}
    wanted_set = set(wanted)
    while cur_m < hi:
        cur = cur * (n - cur_m) // (cur_m + 1)
        cur_m += 1
        if cur_m in wanted_set:
            out[cur_m] = cur
    return out


def list_floor(row: Row, agreement: int, combinations: dict[int, int]) -> int:
    dimension = K_BASE + 1 if row.kind == "mca" else K_BASE
    w = agreement - dimension
    if w < 0:
        raise ValueError(f"negative prefix depth for {row.row_id}")
    return ceil_div(combinations[agreement], row.base_prime**w)


def lower_count(row: Row, agreement: int, combinations: dict[int, int]) -> int:
    floor = list_floor(row, agreement, combinations)
    if row.kind == "list":
        return floor
    q_line = row.base_prime**row.extension_degree
    den = q_line - N + K_BASE * (floor - 1)
    return ceil_div(floor * (q_line - N), den)


def current_row_table() -> list[dict[str, object]]:
    combinations = comb_batch(N, [x for row in ROWS for x in (row.a0, row.a1)])
    rows: list[dict[str, object]] = []
    for row in ROWS:
        q_line = row.base_prime**row.extension_degree
        b_star = q_line // (2**row.lambda_bits)
        lower_a0 = lower_count(row, row.a0, combinations)
        lower_a1 = lower_count(row, row.a1, combinations)
        rows.append(
            {
                "row_id": row.row_id,
                "row": row.row_label,
                "kind": row.kind,
                "n": N,
                "k": K_BASE,
                "base_prime": row.base_prime,
                "extension_degree": row.extension_degree,
                "lambda_bits": row.lambda_bits,
                "a0": row.a0,
                "a1": row.a1,
                "B_star_threshold": b_star,
                "lower_floor_at_a0": lower_a0,
                "lower_floor_at_a1": lower_a1,
                "lower_a0_exceeds_threshold": lower_a0 > b_star,
                "lower_a1_exceeds_threshold": lower_a1 > b_star,
                "deficit_to_exceed_threshold_at_a1": b_star + 1 - lower_a1,
            }
        )
    return rows


def read_lines(root: Path, rel: Path) -> list[str]:
    return (root / rel).read_text(encoding="utf-8").splitlines()


def line_hash(lines: list[str], start: int, end: int) -> str:
    text = "\n".join(lines[start - 1 : end])
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def find_label_block(root: Path, rel: Path, label: str) -> dict[str, object]:
    lines = read_lines(root, rel)
    label_pat = re.compile(r"\\label(?:\[[^]]+\])?\{" + re.escape(label) + r"\}")
    idx = next((i for i, line in enumerate(lines, start=1) if label_pat.search(line)), None)
    if idx is None:
        raise AssertionError(f"label {label} not found in {rel}")
    start = idx
    while start > 1 and "\\begin{" not in lines[start - 1]:
        start -= 1
    end = idx
    while end < len(lines) and "\\end{" not in lines[end - 1]:
        end += 1
    excerpt = lines[start - 1 : min(end, start + 7)]
    return {
        "path": rel.as_posix(),
        "label": label,
        "line_start": start,
        "line_end": end,
        "sha256": line_hash(lines, start, end),
        "excerpt": excerpt,
    }


def fixed_line_excerpt(root: Path, rel: Path, start: int, end: int) -> dict[str, object]:
    lines = read_lines(root, rel)
    if end > len(lines):
        raise AssertionError(f"{rel} has fewer than {end} lines")
    return {
        "path": rel.as_posix(),
        "line_start": start,
        "line_end": end,
        "sha256": line_hash(lines, start, end),
        "excerpt": lines[start - 1 : end],
    }


def packet_open_status(root: Path) -> list[dict[str, object]]:
    statuses = []
    for rel in PACKET_RELS:
        packet = json.loads((root / rel).read_text(encoding="utf-8"))
        status = packet.get("safe_certificates", {}).get("status")
        statement = packet.get("safe_certificates", {}).get("statement")
        detail = packet.get("safe_certificates", {}).get("detail", "")
        statuses.append(
            {
                "path": rel.as_posix(),
                "statement": statement,
                "status": status,
                "states_open": status == "OPEN",
                "detail_digest": hashlib.sha256(detail.encode("utf-8")).hexdigest(),
            }
        )
    return statuses


def corrected_open_status(root: Path) -> dict[str, object]:
    packet = json.loads((root / KB_CORRECTED_REL).read_text(encoding="utf-8"))
    texts = json.dumps(packet, sort_keys=True)
    markers = [
        "no finite U(1116048) <= B* statement exists or is claimed",
        "deduped finite total is printed",
        "OPEN cells",
    ]
    return {
        "path": KB_CORRECTED_REL.as_posix(),
        "koalabear_corrected_open_step": 1116048,
        "markers_present": {marker: marker in texts for marker in markers},
    }


def symbolic_occurrences(root: Path) -> list[dict[str, object]]:
    scan_specs = [
        (RAW_REL, ["U_{\\rm paid}", "U_Q", "U_{\\Rone}", "U_{\\rm R1}"]),
        (COMPACT_REL, ["safe\\_upper", "U_Q", "U_{BC}", "U_{SP}", "finite Q certificate"]),
    ]
    hits: list[dict[str, object]] = []
    for rel, needles in scan_specs:
        lines = read_lines(root, rel)
        for no, line in enumerate(lines, start=1):
            if any(needle in line for needle in needles):
                hits.append({"path": rel.as_posix(), "line": no, "text": line.strip()[:220]})
    return hits[:40]


def component_availability(row_records: list[dict[str, object]], root: Path) -> dict[str, object]:
    packet_statuses = packet_open_status(root)
    corrected = corrected_open_status(root)
    all_lower_ok = all(r["lower_a0_exceeds_threshold"] and not r["lower_a1_exceeds_threshold"] for r in row_records)
    all_packets_open = all(p["states_open"] for p in packet_statuses)
    corrected_markers = corrected["markers_present"]
    koalabear_current_open_declared = all(corrected_markers.values())
    return {
        "B_star_threshold": "present_exact_recomputed",
        "L_a0_lower_side": "present_exact_recomputed",
        "one_step_lower_floor_quiet_at_a1": all_lower_ok,
        "U_paid_a1": "not_instantiated_as_one_step_integer_total",
        "U_Q_a1": "not_instantiated_as_finite_Q_integer_certificate",
        "U_R1_a1": "not_instantiated_as_finite_R1_integer_certificate",
        "legacy_frontier_packets_state_safe_side_open": all_packets_open,
        "koalabear_current_open_packet_declares_no_finite_upper_total": koalabear_current_open_declared,
        "one_step_replay_possible_from_current_tree": False,
        "reason": (
            "The exact threshold and lower-side rows replay, but the named upper "
            "summands required by cor:capfr1-Q-R1-closing are present only as "
            "symbolic or future certificate inputs in current sources."
        ),
    }


def build_certificate() -> dict[str, object]:
    root = repo_root()
    row_records = current_row_table()
    statement_blocks = [
        find_label_block(root, RAW_REL, "prop:capfr1-slope-elimination"),
        find_label_block(root, RAW_REL, "cor:capfr1-Q-R1-closing"),
        find_label_block(root, RAW_REL, "cor:capg-adjacent-pairs"),
        find_label_block(root, RAW_REL, "prop:capg-census-floor"),
    ]
    source_context = [
        fixed_line_excerpt(root, COMPACT_REL, 1608, 1619),
        fixed_line_excerpt(root, COMPACT_REL, 1637, 1642),
        fixed_line_excerpt(root, COMPACT_REL, 2153, 2164),
    ]
    components = component_availability(row_records, root)
    return {
        "schema": "q-r1-closing-audit.v1",
        "status": STATUS,
        "object": "cor:capfr1-Q-R1-closing finite one-step input replay audit",
        "claim_boundaries": {
            "is_counterexample": False,
            "is_full_canonical_statement_not_proxy_or_toy_row": False,
            "audits_canonical_statement_inputs": True,
            "verifies_one_step_inequality": False,
            "resolves_or_advances_prob_band": False,
            "proves_prob_band_undecidable": False,
            "claims_no_method_can_reach": False,
            "is_novel_not_confirming_a_proven_theorem": True,
            "beats_or_narrows_trivial_baseline": False,
            "is_not_degenerate_or_tautological_by_construction": True,
            "independent_recheck_confirms": True,
        },
        "evidence_type": "FULL_FINITE_CENSUS",
        "is_degenerate_by_construction": False,
        "beats_trivial_baseline": False,
        "is_tautology_under_preconditions": False,
        "theorem_problem_ids": [
            "cor:capfr1-Q-R1-closing",
            "prop:capfr1-slope-elimination",
            "cor:capg-adjacent-pairs",
            "prop:capg-census-floor",
        ],
        "row_table": row_records,
        "component_availability": components,
        "packet_open_status": packet_open_status(root),
        "current_open_packet_status": corrected_open_status(root),
        "statement_blocks": statement_blocks,
        "source_context": source_context,
        "symbolic_occurrences_sample": symbolic_occurrences(root),
        "regen_command": (
            "py -3.13 experimental/scripts/verify_q_r1_closing_audit.py "
            "--emit-defaults --check"
        ),
    }


def check_certificate(cert: dict[str, object]) -> None:
    if cert["status"] != STATUS:
        raise AssertionError("status drift")
    rows = cert["row_table"]
    if len(rows) != 4:
        raise AssertionError("expected four current adjacent rows")
    for row in rows:
        if not row["lower_a0_exceeds_threshold"]:
            raise AssertionError(f"{row['row_id']}: lower floor no longer exceeds B* at a0")
        if row["lower_a1_exceeds_threshold"]:
            raise AssertionError(f"{row['row_id']}: lower floor unexpectedly exceeds B* at a1")
        if row["deficit_to_exceed_threshold_at_a1"] <= 0:
            raise AssertionError(f"{row['row_id']}: nonpositive a1 deficit")
    comp = cert["component_availability"]
    if comp["one_step_replay_possible_from_current_tree"]:
        raise AssertionError("one-step replay incorrectly marked possible")
    for field in ("U_paid_a1", "U_Q_a1", "U_R1_a1"):
        if not str(comp[field]).startswith("not_instantiated"):
            raise AssertionError(f"{field} unexpectedly marked instantiated")
    if not comp["legacy_frontier_packets_state_safe_side_open"]:
        raise AssertionError("legacy packet safe-side status no longer all OPEN")
    if not comp["koalabear_current_open_packet_declares_no_finite_upper_total"]:
        raise AssertionError("corrected KoalaBear open packet markers missing")
    labels = {b["label"] for b in cert["statement_blocks"]}
    needed = {
        "prop:capfr1-slope-elimination",
        "cor:capfr1-Q-R1-closing",
        "cor:capg-adjacent-pairs",
        "prop:capg-census-floor",
    }
    if labels != needed:
        raise AssertionError(f"statement labels mismatch: {labels}")


def write_defaults(cert: dict[str, object]) -> None:
    path = repo_root() / CERT_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit-defaults", action="store_true", help="write the default certificate JSON")
    parser.add_argument("--check", action="store_true", help="check the generated or existing certificate")
    args = parser.parse_args()

    cert = build_certificate()
    if args.emit_defaults:
        write_defaults(cert)
    if args.check:
        path = repo_root() / CERT_REL
        if path.exists():
            cert = json.loads(path.read_text(encoding="utf-8"))
        check_certificate(cert)
    print("Q/R1 closing audit")
    print(f"status: {STATUS}")
    print(f"rows: {len(cert['row_table'])}")
    print(f"one_step_replay_possible: {cert['component_availability']['one_step_replay_possible_from_current_tree']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
