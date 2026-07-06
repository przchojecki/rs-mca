#!/usr/bin/env python3
"""Verify the KB-MCA L4 BC base-field floor ladder.

Status: AUDIT / EXACT_ARITHMETIC.  This packet does not prove the BC
split-pencil upper census and does not certify U(a0+1) <= B*.  It only pins the
finite L4 conventions and the exact base-field floor that any BC model must
include at the first interior profiles.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from math import comb
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "bc-l4-base-floor-ladder-v1"
THEOREM_PROBLEM_ID = "conj:BC first interior base-field floor; KB-MCA L4"
DEFAULT_OUTPUT = Path(
    "experimental/data/certificates/frontier-adjacent/"
    "kb_mca_bc_l4_base_floor_ladder_v1.json"
)
NOTE_PATH = "experimental/notes/thresholds/cap25_v13_bc_l4_base_floor_ladder.md"

P_KB = 2**31 - 2**24 + 1
N0 = 2**21
K0_RS = 2**20
K0_MCA = K0_RS + 1
SCALE = 16
N = N0 // SCALE
M = 1_116_048 // SCALE
K = (K0_MCA + SCALE - 1) // SCALE
W = M - K
BOUNDARY_D1 = W + 1
K_RAW = 4_807_520
B_STAR = 274_980_728_111_395_087
OFFSETS = tuple(range(0, 9))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def ceil_div(numer: int, denom: int) -> int:
    return -(-numer // denom)


def log2_int(value: int) -> float:
    # Stable enough for display fields only; all verdicts below use integers.
    bits = value.bit_length()
    shift = max(bits - 53, 0)
    mantissa = value >> shift
    return shift + math.log2(mantissa)


def sha256_payload(payload: dict[str, Any]) -> str:
    clone = json.loads(json.dumps(payload, sort_keys=True))
    clone.pop("payload_sha256", None)
    blob = json.dumps(clone, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def profile_row(offset: int) -> dict[str, Any]:
    # offset=0 is the Q boundary profile.  BC starts at offset=1.
    d1 = BOUNDARY_D1 + offset
    d2 = N - K + 1 - d1
    m_prime = K - 1 + d1
    prefix_depth = d1 - 1
    prefix_denominator = P_KB**prefix_depth
    level_supports = comb(N, m_prime)
    heaviest_prefix_floor = ceil_div(level_supports, prefix_denominator)
    multiplier = comb(m_prime, M)
    base_floor = heaviest_prefix_floor * multiplier
    density_numer = level_supports * multiplier
    density_denom = prefix_denominator
    return {
        "offset_from_boundary": offset,
        "profile_role": "Q_BOUNDARY_NOT_BC" if offset == 0 else "BC_INTERIOR",
        "d1": d1,
        "d2": d2,
        "m_prime": m_prime,
        "prefix_depth_d1_minus_1": prefix_depth,
        "conditions": {
            "m_le_m_prime": M <= m_prime,
            "m_prime_plus_d1_le_n": m_prime + d1 <= N,
            "interior_d1_ge_w_plus_2": d1 >= W + 2,
            "d1_le_half_n_minus_K_plus_1": d1 <= (N - K + 1) // 2,
        },
        "level_supports_choose_n_mprime": str(level_supports),
        "prefix_denominator_p_power": str(prefix_denominator),
        "prefix_average_log2_approx": round(log2_int(level_supports) - log2_int(prefix_denominator), 6),
        "heaviest_prefix_floor_ceil": heaviest_prefix_floor,
        "binomial_subsupport_multiplier_choose_mprime_m": str(multiplier),
        "base_field_floor_exact": str(base_floor),
        "base_field_floor_log2_approx": round(log2_int(base_floor), 6),
        "density_model": {
            "numerator": str(density_numer),
            "denominator": str(density_denom),
            "log2_approx": round(log2_int(density_numer) - log2_int(density_denom), 6),
            "below_one": density_numer < density_denom,
        },
        "orientation_only": {
            "exceeds_K_raw_integer_multiplier": base_floor > K_RAW,
            "exceeds_B_star_absolute_budget": base_floor > B_STAR,
        },
    }


def build_payload() -> dict[str, Any]:
    rows = [profile_row(offset) for offset in OFFSETS]
    payload: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "theorem_problem_id": THEOREM_PROBLEM_ID,
        "proof_status": "AUDIT / EXACT_ARITHMETIC",
        "companion_note": NOTE_PATH,
        "claim": (
            "Exact arithmetic for the KB-MCA L4 quotient row's BC boundary and "
            "first interior base-field floor profiles."
        ),
        "row": {
            "source": "kb_mca_conjq_rung_audit_v1 L4 row, read through agents.md's finite BC split-pencil certificate target",
            "base_prime_p": P_KB,
            "scale": SCALE,
            "n": N,
            "m": M,
            "K_effective_MCA": K,
            "w_bc": W,
            "q_boundary_d1": BOUNDARY_D1,
            "first_bc_interior_d1": BOUNDARY_D1 + 1,
            "m_is_odd": M % 2 == 1,
            "zero_ladder_correction": M % 2 == 1,
            "K_raw_from_Q_packet": K_RAW,
            "B_star": B_STAR,
        },
        "convention_checks": {
            "K_effective_equals_ceil_original_MCA_K_over_scale": K == (K0_MCA + SCALE - 1) // SCALE,
            "w_matches_integrated_Q_L4_depth": W == 4216,
            "boundary_d1_is_w_plus_1": BOUNDARY_D1 == W + 1,
            "bc_starts_at_w_plus_2": BOUNDARY_D1 + 1 == W + 2,
        },
        "profile_rows": rows,
        "findings": [
            "The L4 BC target uses K=ceil((2^20+1)/16)=65537, so w=m-K=4216.",
            "The Q boundary profile is d1=w+1=4217; BC's first interior profile is d1=w+2=4218.",
            "At the first interior profiles the prefix-fiber density model is already below one, so the exact base-field floor is driven by the integer ceiling heaviest_prefix_floor>=1.",
            "The orientation comparisons to K_raw and B* are not ledger payments and are not safe/unsafe verdicts.",
        ],
        "non_claims": [
            "No proof of conj:BC is claimed.",
            "No upper bound on primitive split-pencil cells is claimed.",
            "No safe certificate U(1116048)<=B* is claimed.",
            "The orientation_only comparisons are displayed to prevent scale confusion; support-census floors are not bad-slope counts.",
        ],
    }
    payload["payload_sha256"] = sha256_payload(payload)
    return payload


def check_payload(payload: dict[str, Any]) -> None:
    expected = build_payload()
    require(payload == expected, "payload mismatch against exact recomputation")
    require(payload["payload_sha256"] == sha256_payload(payload), "payload hash mismatch")
    rows = payload["profile_rows"]
    require(rows[0]["profile_role"] == "Q_BOUNDARY_NOT_BC", "offset 0 must be boundary")
    require(rows[1]["profile_role"] == "BC_INTERIOR", "offset 1 must be interior")
    require(rows[1]["d1"] == W + 2, "first interior d1 mismatch")
    require(rows[1]["heaviest_prefix_floor_ceil"] == 1, "first interior ceiling floor should be 1")
    require(rows[2]["orientation_only"]["exceeds_K_raw_integer_multiplier"], "offset 2 should exceed K_raw orientation")


def tamper_selftest(path: Path) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    bad = json.loads(json.dumps(payload))
    bad["profile_rows"][1]["d1"] += 1
    try:
        check_payload(bad)
    except AssertionError:
        return
    raise AssertionError("tamper self-test failed to catch modified d1")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit-defaults", action="store_true", help="write the default certificate JSON")
    parser.add_argument("--check", type=Path, default=None, help="certificate JSON to verify")
    parser.add_argument("--tamper-selftest", action="store_true", help="verify that a local tamper is rejected")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.emit_defaults:
        payload = build_payload()
        DEFAULT_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        DEFAULT_OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"wrote {DEFAULT_OUTPUT.as_posix()}")
    check_path = args.check or DEFAULT_OUTPUT
    payload = json.loads(check_path.read_text(encoding="utf-8"))
    check_payload(payload)
    if args.tamper_selftest:
        tamper_selftest(check_path)
    print(
        "bc_l4_base_floor_ladder: "
        f"status=AUDIT result=PASS file={check_path.as_posix()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
