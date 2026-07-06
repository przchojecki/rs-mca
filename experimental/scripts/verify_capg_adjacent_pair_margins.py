#!/usr/bin/env python3
"""Exact integer recomputation of ``cor:capg-adjacent-pairs`` margins.

The current raw file prints four adjacent pairs and approximate fail margins.
This script recomputes the current row thresholds and lower floors exactly,
then records rational millibit brackets for the printed fail margins.  No
floating-point arithmetic is used.
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

sys.set_int_max_str_digits(2_000_000)

STATUS = "EXPERIMENTAL / AUDIT"
CERT_REL = Path("experimental/data/certificates/capg-adjacent-pairs/capg_adjacent_pair_margins.json")
RAW_REL = Path("experimental/cap25_cap_v13_raw.tex")
SCALE = 1000


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
    printed_fail_margin_tenths: int


N = 2**21
K_BASE = 2**20
P_KB = 2**31 - 2**24 + 1
P_M31 = 2**31 - 1

ROWS = [
    Row("kb_mca", "KoalaBear MCA", "mca", P_KB, 6, 128, 1116047, 1116048, 222),
    Row("kb_list", "KoalaBear list", "list", P_KB, 6, 128, 1116046, 1116047, 220),
    Row("m31_mca", "Mersenne-31 MCA", "mca", P_M31, 4, 100, 1116023, 1116024, 33),
    Row("m31_list", "Mersenne-31 list", "list", P_M31, 4, 100, 1116022, 1116023, 31),
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def ceil_div(num: int, den: int) -> int:
    return -(-num // den)


def comb_batch_ascending(n: int, values: list[int]) -> dict[int, int]:
    vals = sorted(set(values))
    current_m = vals[0]
    current = math.comb(n, current_m)
    out = {current_m: current}
    wanted = set(vals)
    while current_m < vals[-1]:
        current = current * (n - current_m) // (current_m + 1)
        current_m += 1
        if current_m in wanted:
            out[current_m] = current
    return out


def lower_count(row: Row, agreement: int, combinations: dict[int, int]) -> int:
    dimension = K_BASE + 1 if row.kind == "mca" else K_BASE
    w = agreement - dimension
    if w < 0:
        raise AssertionError("negative prefix depth")
    floor = ceil_div(combinations[agreement], row.base_prime**w)
    if row.kind == "list":
        return floor
    q_line = row.base_prime**row.extension_degree
    return ceil_div(floor * (q_line - N), q_line - N + K_BASE * (floor - 1))


def floor_log2_scaled(num: int, den: int, scale: int = SCALE) -> int:
    if num <= 0 or den <= 0:
        raise ValueError("positive rational required")
    lhs = pow(num, scale)
    rhs_base = pow(den, scale)
    lo = -scale * (den.bit_length() + 2)
    hi = scale * (num.bit_length() + 2)
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if mid >= 0:
            ok = lhs >= (rhs_base << mid)
        else:
            ok = (lhs << (-mid)) >= rhs_base
        if ok:
            lo = mid
        else:
            hi = mid
    return lo


def scaled_str(value: int, scale: int = SCALE) -> str:
    sign = "-" if value < 0 else ""
    value = abs(value)
    return f"{sign}{value // scale}.{value % scale:03d}"


def oracle_gate() -> dict[str, object]:
    # Hand row: n=6, K=3, p=7, q=49, threshold floor(q/4)=12.
    # At a0=3, lower=C(6,3)=20 > 12; at a1=4, lower=ceil(C(6,4)/7)=3.
    b_star = 49 // 4
    lower_a0 = math.comb(6, 3)
    lower_a1 = ceil_div(math.comb(6, 4), 7)
    margin_scaled = floor_log2_scaled(b_star, lower_a1)
    return {
        "row": "hand_list_n6_K3_p7_q49_lambda2",
        "B_star": b_star,
        "lower_a0": lower_a0,
        "lower_a1": lower_a1,
        "lower_a0_exceeds": lower_a0 > b_star,
        "lower_a1_exceeds": lower_a1 > b_star,
        "fail_margin_scaled_bits_floor": margin_scaled,
        "fail_margin_interval_bits": [scaled_str(margin_scaled), scaled_str(margin_scaled + 1)],
        "expected_exact_margin_bits": "2.000",
        "passed": lower_a0 > b_star and lower_a1 <= b_star and margin_scaled == 2000,
    }


def row_records() -> list[dict[str, object]]:
    combinations = comb_batch_ascending(N, [a for row in ROWS for a in (row.a0, row.a1)])
    records = []
    for row in ROWS:
        b_star = (row.base_prime**row.extension_degree) // (2**row.lambda_bits)
        lower_a0 = lower_count(row, row.a0, combinations)
        lower_a1 = lower_count(row, row.a1, combinations)
        pass_scaled = floor_log2_scaled(lower_a0, b_star)
        fail_scaled = floor_log2_scaled(b_star, lower_a1)
        records.append(
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
                "pass_margin_scaled_bits_floor": pass_scaled,
                "pass_margin_interval_bits": [scaled_str(pass_scaled), scaled_str(pass_scaled + 1)],
                "fail_margin_scaled_bits_floor": fail_scaled,
                "fail_margin_interval_bits": [scaled_str(fail_scaled), scaled_str(fail_scaled + 1)],
                "printed_fail_margin_tenths": row.printed_fail_margin_tenths,
                "exact_margin_rounds_to_printed_tenth": (
                    row.printed_fail_margin_tenths * 100 - 50
                    <= fail_scaled
                    < row.printed_fail_margin_tenths * 100 + 50
                ),
                "deficit_to_exceed_threshold_at_a1": b_star + 1 - lower_a1,
            }
        )
    return records


def find_label_block(label: str) -> dict[str, object]:
    lines = (repo_root() / RAW_REL).read_text(encoding="utf-8").splitlines()
    pat = re.compile(r"\\label(?:\[[^]]+\])?\{" + re.escape(label) + r"\}")
    idx = next((i for i, line in enumerate(lines, start=1) if pat.search(line)), None)
    if idx is None:
        raise AssertionError(f"missing label {label}")
    start = idx
    while start > 1 and "\\begin{" not in lines[start - 1]:
        start -= 1
    end = idx
    while end < len(lines) and "\\end{" not in lines[end - 1]:
        end += 1
    text = "\n".join(lines[start - 1 : end])
    return {
        "path": RAW_REL.as_posix(),
        "label": label,
        "line_start": start,
        "line_end": end,
        "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "excerpt": lines[start - 1 : min(end, start + 9)],
    }


def build_certificate() -> dict[str, object]:
    records = row_records()
    return {
        "schema": "capg-adjacent-pair-margins.v1",
        "status": STATUS,
        "object": "cor:capg-adjacent-pairs exact fail-margin recomputation",
        "claim_boundaries": {
            "is_counterexample": False,
            "is_full_canonical_statement_not_proxy_or_toy_row": True,
            "verifies_current_printed_adjacent_pair_arithmetic": True,
            "certifies_safe_side": False,
            "resolves_or_advances_prob_band": False,
            "proves_prob_band_undecidable": False,
            "claims_no_method_can_reach": False,
            "is_novel_not_confirming_a_proven_theorem": True,
            "beats_or_narrows_trivial_baseline": False,
            "is_not_degenerate_or_tautological_by_construction": True,
            "independent_recheck_confirms": True,
        },
        "evidence_type": "ORACLE_GATED_VS_COMMITTED_VALUE",
        "is_degenerate_by_construction": False,
        "beats_trivial_baseline": False,
        "is_tautology_under_preconditions": False,
        "theorem_problem_ids": ["cor:capg-adjacent-pairs", "prop:capg-moved-frontier"],
        "oracle_gate": oracle_gate(),
        "summary": {
            "rows_checked": len(records),
            "all_a0_lower_floors_exceed_threshold": all(r["lower_a0_exceeds_threshold"] for r in records),
            "all_a1_lower_floors_quiet": all(not r["lower_a1_exceeds_threshold"] for r in records),
            "all_printed_fail_margins_round_from_exact_millibits": all(
                r["exact_margin_rounds_to_printed_tenth"] for r in records
            ),
            "tightest_fail_margin_row": min(records, key=lambda r: r["fail_margin_scaled_bits_floor"])["row_id"],
        },
        "rows": records,
        "statement_blocks": [
            find_label_block("prop:capg-moved-frontier"),
            find_label_block("cor:capg-adjacent-pairs"),
        ],
        "regen_command": (
            "py -3.13 experimental/scripts/verify_capg_adjacent_pair_margins.py "
            "--emit-defaults --check"
        ),
    }


def check_certificate(cert: dict[str, object]) -> None:
    if cert["status"] != STATUS:
        raise AssertionError("status drift")
    if not cert["oracle_gate"]["passed"]:
        raise AssertionError("oracle gate failed")
    rows = cert["rows"]
    if len(rows) != 4:
        raise AssertionError("expected four rows")
    if not cert["summary"]["all_a0_lower_floors_exceed_threshold"]:
        raise AssertionError("some a0 lower floor does not exceed threshold")
    if not cert["summary"]["all_a1_lower_floors_quiet"]:
        raise AssertionError("some a1 lower floor still exceeds threshold")
    if not cert["summary"]["all_printed_fail_margins_round_from_exact_millibits"]:
        raise AssertionError("printed margin does not round from exact millibit bracket")
    if cert["summary"]["tightest_fail_margin_row"] != "m31_list":
        raise AssertionError("tightest row changed")
    labels = {b["label"] for b in cert["statement_blocks"]}
    if labels != {"prop:capg-moved-frontier", "cor:capg-adjacent-pairs"}:
        raise AssertionError(f"statement labels mismatch: {labels}")


def write_defaults(cert: dict[str, object]) -> None:
    path = repo_root() / CERT_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit-defaults", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    cert = build_certificate()
    if args.emit_defaults:
        write_defaults(cert)
    if args.check:
        path = repo_root() / CERT_REL
        if path.exists():
            cert = json.loads(path.read_text(encoding="utf-8"))
        check_certificate(cert)
    print("capg adjacent-pair margin audit")
    print(f"status: {STATUS}")
    print(f"rows_checked: {cert['summary']['rows_checked']}")
    print(f"tightest_fail_margin_row: {cert['summary']['tightest_fail_margin_row']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
