#!/usr/bin/env python3
"""Independent integer replay for the quotient-pair plane-218 packet."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "experimental/data/certificates/kb-mca-rank11-quotient-pair-plane218-v1/contract.json"
CONTRACT_SHA256 = "0d72cc299765c6b30b2fd517379b4ae4384d0f9ba3058b1028b9d433bff24656"


def check(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def first_integer_at_least(numerator: int, denominator: int) -> int:
    candidate = numerator // denominator
    if candidate * denominator < numerator:
        candidate += 1
    return candidate


def main() -> None:
    payload = CONTRACT.read_bytes()
    check(hashlib.sha256(payload).hexdigest() == CONTRACT_SHA256, "contract hash")
    data = json.loads(payload)
    row = data["row"]
    source = data["source_interface"]
    cap = data["plane_cap"]
    router = data["dimension_router"]
    bank = data["endpoint_bank"]

    n = row["n"]
    degree = row["K"]
    core_size = row["pair_core_size"]
    line_cap = source["affine_line_cap"]

    cap_rhs = 219 * core_size - line_cap * n
    c219 = cap["common_core_floor"]
    check((219 - line_cap) * (c219 - 1) < cap_rhs <= (219 - line_cap) * c219,
          "219-core ceiling identity")
    cap_k = degree - c219
    for kprime in range(1, cap_k + 1):
        full_floor = 95866 + 205 * kprime
        full_capacity = 219 * (kprime - 1)
        check(full_floor - full_capacity >= 30705, f"219 contradiction {kprime}")

    common_rhs = 520 * core_size - 218 * n
    common = router["dimension_three_core_floor"]
    check((520 - 218) * (common - 1) < common_rhs <= (520 - 218) * common,
          "dimension-three core ceiling identity")
    check(218 * router["shortened_n"] - 520 * router["shortened_pair_core"] == 178,
          "dimension-three incidence slack")
    check(router["dimension_four_heavy_record_floor"] == 219 * 29,
          "dimension-four record floor")

    bank_rhs = 218 * core_size - line_cap * n
    c218 = bank["common_core_floor"]
    check((218 - line_cap) * (c218 - 1) < bank_rhs <= (218 - line_cap) * c218,
          "218-core ceiling identity")
    first_feasible = None
    direction_minimum = 10**9
    degree_deficit_maximum = -1
    saturation_minimum = Fraction(10, 1)
    scanned = 0
    for kprime in range(1, bank["shortened_K_ceiling"] + 1):
        full = 28396 + 204 * kprime
        capacity = 218 * (kprime - 1)
        if full > capacity:
            continue
        if first_feasible is None:
            first_feasible = kprime
        scanned += 1
        directions = first_integer_at_least(full, kprime - 1)
        direction_minimum = min(direction_minimum, directions)
        degree_deficit_maximum = max(degree_deficit_maximum, capacity - full)
        saturation_minimum = min(saturation_minimum, Fraction(full, capacity))

    check(first_feasible == bank["shortened_K_floor"] == 2044, "first feasible endpoint")
    check(scanned == 5025 - 2044 + 1 == 2982, "endpoint scan size")
    check(direction_minimum == bank["projective_direction_floor"] == 210, "direction minimum")
    check(degree_deficit_maximum == bank["aggregate_degree_deficit_ceiling"] == 41736,
          "deficit maximum")
    check(saturation_minimum == Fraction(bank["saturation_numerator"],
                                         bank["saturation_denominator"]),
          "saturation minimum")
    check(saturation_minimum > Fraction(9618, 10000), "saturation decimal claim")
    check(218 * 217 // 2 - 210 * (15 * 14 // 2) ==
          bank["dual_remaining_pair_ceiling"] == 1603, "dual pair budget")

    note = " ".join(
        (ROOT / "experimental/notes/thresholds/kb_mca_rank11_quotient_pair_plane218_v1.md")
        .read_text()
        .split()
    )
    check("does not assert that the current rank-eleven route has already produced" in note,
          "source-interface nonclaim")
    check("positive-characteristic line arrangements need" in note,
          "characteristic boundary")
    check("Neither output is paid" in note, "payment nonclaim")
    print(
        "KB_RANK11_QUOTIENT_PAIR_PLANE218_INDEPENDENT_PASS "
        f"states={scanned} directions={direction_minimum} pairs=1603"
    )


if __name__ == "__main__":
    main()
